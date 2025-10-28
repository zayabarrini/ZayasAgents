# monitoring.tf
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  provider = aws.eu_central

  alarm_name          = "app-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors EC2 CPU utilization"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}

resource "aws_cloudwatch_metric_alarm" "http_5xx_errors" {
  provider = aws.eu_central

  alarm_name          = "alb-http-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "High number of 5XX errors from targets"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    LoadBalancer = aws_lb.app_emea.arn_suffix
  }
}

# Lambda function for auto-remediation
resource "aws_lambda_function" "incident_remediation" {
  provider = aws.eu_central

  filename      = "remediation_lambda.zip"
  function_name = "incident-remediation"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "python3.9"

  environment {
    variables = {
      ASG_NAME = aws_autoscaling_group.app.name
    }
  }
}

# EventBridge rule for automatic incident response
resource "aws_cloudwatch_event_rule" "incident_detection" {
  provider = aws.eu_central

  name        = "incident-detection"
  description = "Trigger remediation for production incidents"

  event_pattern = jsonencode({
    source      = ["aws.cloudwatch"]
    detail-type = ["CloudWatch Alarm State Change"]
    detail = {
      alarmName = [aws_cloudwatch_metric_alarm.high_cpu.alarm_name]
      state = {
        value = ["ALARM"]
      }
    }
  })
}