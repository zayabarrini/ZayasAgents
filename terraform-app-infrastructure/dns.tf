# dns.tf
resource "aws_route53_zone" "primary" {
  name = "app-global.com"
}

# Primary EMEA record
resource "aws_route53_record" "app_emea" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "app.app-global.com"
  type    = "A"

  alias {
    name                   = aws_lb.app_emea.dns_name
    zone_id                = aws_lb.app_emea.zone_id
    evaluate_target_health = true
  }
}

# Geo-location routing for China (commented out - requires special setup)
/*
resource "aws_route53_record" "app_china" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "app.app-global.com"
  type    = "A"

  geolocation_routing_policy {
    country = "CN"
  }

  set_identifier = "China"
  alias {
    name                   = "china-specific-alias" # Would point to China CDN
    zone_id                = "china-zone-id"
    evaluate_target_health = true
  }
}
*/