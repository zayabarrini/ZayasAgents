from typing import Dict, Optional
from ..core.constants import Language


class MultiLanguageSupport:
    def __init__(self):
        self.translations = self._load_translations()

    def get_message(
        self,
        message_key: str,
        language: Language,
        placeholders: Optional[Dict[str, str]] = None,
    ) -> str:
        translation = self.translations.get(language.value, {}).get(
            message_key, self.translations["en"].get(message_key, message_key)
        )

        if placeholders:
            for key, value in placeholders.items():
                translation = translation.replace(f"{{{key}}}", str(value))

        return translation

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        return {
            "en": {
                "payment_success": "Payment of {amount} {currency} completed successfully. Transaction ID: {transaction_id}",
                "payment_failed": "Payment failed: {reason}",
                "confirmation_required": "Please confirm your payment of {amount} {currency} to {recipient}",
                "security_check_failed": "Security verification failed. Please contact support.",
                "compliance_check_failed": "Additional verification required. Please provide: {documents}",
                "amount_exceeds_limit": "Payment amount exceeds the limit for {country}",
                "currency_conversion_note": "Amount will be converted from {from_currency} to {to_currency}",
            },
            "es": {
                "payment_success": "Pago de {amount} {currency} completado exitosamente. ID de transacción: {transaction_id}",
                "payment_failed": "Pago fallido: {reason}",
                "confirmation_required": "Por favor confirme su pago de {amount} {currency} a {recipient}",
                "security_check_failed": "Verificación de seguridad fallida. Por favor contacte al soporte.",
                "compliance_check_failed": "Verificación adicional requerida. Por favor proporcione: {documents}",
                "amount_exceeds_limit": "El monto del pago excede el límite para {country}",
                "currency_conversion_note": "El monto será convertido de {from_currency} a {to_currency}",
            },
            "fr": {
                "payment_success": "Paiement de {amount} {currency} effectué avec succès. ID de transaction: {transaction_id}",
                "payment_failed": "Paiement échoué: {reason}",
                "confirmation_required": "Veuillez confirmer votre paiement de {amount} {currency} à {recipient}",
                "security_check_failed": "Échec de la vérification de sécurité. Veuillez contacter le support.",
                "compliance_check_failed": "Vérification supplémentaire requise. Veuillez fournir: {documents}",
                "amount_exceeds_limit": "Le montant du paiement dépasse la limite pour {country}",
                "currency_conversion_note": "Le montant sera converti de {from_currency} à {to_currency}",
            },
            "de": {
                "payment_success": "Zahlung von {amount} {currency} erfolgreich abgeschlossen. Transaktions-ID: {transaction_id}",
                "payment_failed": "Zahlung fehlgeschlagen: {reason}",
                "confirmation_required": "Bitte bestätigen Sie Ihre Zahlung von {amount} {currency} an {recipient}",
                "security_check_failed": "Sicherheitsüberprüfung fehlgeschlagen. Bitte kontaktieren Sie den Support.",
                "compliance_check_failed": "Zusätzliche Überprüfung erforderlich. Bitte提供: {documents}",
                "amount_exceeds_limit": "Der Zahlungsbetrag überschreitet das Limit für {country}",
                "currency_conversion_note": "Betrag wird von {from_currency} in {to_currency} umgerechnet",
            },
            "ru": {
                "payment_success": "Платеж на сумму {amount} {currency} успешно завершен. ID транзакции: {transaction_id}",
                "payment_failed": "Ошибка платежа: {reason}",
                "confirmation_required": "Пожалуйста, подтвердите ваш платеж на сумму {amount} {currency} получателю {recipient}",
                "security_check_failed": "Проверка безопасности не пройдена. Свяжитесь со службой поддержки.",
                "compliance_check_failed": "Требуется дополнительная проверка. Пожалуйста, предоставьте: {documents}",
                "amount_exceeds_limit": "Сумма платежа превышает лимит для {country}",
                "currency_conversion_note": "Сумма будет конвертирована из {from_currency} в {to_currency}",
            },
            "ja": {
                "payment_success": "{amount} {currency}の支払いが正常に完了しました。取引ID: {transaction_id}",
                "payment_failed": "支払い失敗: {reason}",
                "confirmation_required": "{recipient}への{amount} {currency}の支払いを確認してください",
                "security_check_failed": "セキュリティ確認に失敗しました。サポートにお問い合わせください。",
                "compliance_check_failed": "追加の確認が必要です。以下を提供してください: {documents}",
                "amount_exceeds_limit": "支払額が{country}の制限を超えています",
                "currency_conversion_note": "金額は{from_currency}から{to_currency}に変換されます",
            },
            "ko": {
                "payment_success": "{amount} {currency} 결제가 성공적으로 완료되었습니다. 거래 ID: {transaction_id}",
                "payment_failed": "결제 실패: {reason}",
                "confirmation_required": "{recipient}에게 {amount} {currency} 결제를 확인해 주세요",
                "security_check_failed": "보안 검증에 실패했습니다. 지원팀에 문의하세요.",
                "compliance_check_failed": "추가 검증이 필요합니다. 다음을 제공해 주세요: {documents}",
                "amount_exceeds_limit": "결제 금액이 {country}의 한도를 초과합니다",
                "currency_conversion_note": "금액이 {from_currency}에서 {to_currency}로 변환됩니다",
            },
            "ar": {
                "payment_success": "تم completado بنجاح دفعة {amount} {currency}. معرف المعاملة: {transaction_id}",
                "payment_failed": "فشل الدفع: {reason}",
                "confirmation_required": "يرجى تأكيد دفعتك البالغة {amount} {currency} إلى {recipient}",
                "security_check_failed": "فشل التحقق الأمني. يرجى الاتصال بالدعم.",
                "compliance_check_failed": "مطلوب تحقق إضافي. يرجى تقديم: {documents}",
                "amount_exceeds_limit": "مبلغ الدفع يتجاوز الحد المسموح به لـ {country}",
                "currency_conversion_note": "سيتم تحويل المبلغ من {from_currency} إلى {to_currency}",
            },
            "hi": {
                "payment_success": "{amount} {currency} का भुगतान सफलतापूर्वक पूरा हुआ। लेनदेन आईडी: {transaction_id}",
                "payment_failed": "भुगतान विफल: {reason}",
                "confirmation_required": "कृपया {recipient} को {amount} {currency} के अपने भुगतान की पुष्टि करें",
                "security_check_failed": "सुरक्षा सत्यापन विफल। कृपया सहायता से संपर्क करें।",
                "compliance_check_failed": "अतिरिक्त सत्यापन आवश्यक है। कृपया प्रदान करें: {documents}",
                "amount_exceeds_limit": "भुगतान राशि {country} की सीमा से अधिक है",
                "currency_conversion_note": "राशि {from_currency} से {to_currency} में परिवर्तित की जाएगी",
            },
            "it": {
                "payment_success": "Pagamento di {amount} {currency} completato con successo. ID transazione: {transaction_id}",
                "payment_failed": "Pagamento fallito: {reason}",
                "confirmation_required": "Si prega di confermare il pagamento di {amount} {currency} a {recipient}",
                "security_check_failed": "Verifica di sicurezza fallita. Si prega di contattare l'assistenza.",
                "compliance_check_failed": "Verifica aggiuntiva richiesta. Si prega di fornire: {documents}",
                "amount_exceeds_limit": "L'importo del pagamento supera il limite per {country}",
                "currency_conversion_note": "L'importo sarà convertito da {from_currency} a {to_currency}",
            },
            "zh": {
                "payment_success": "成功完成{amount} {currency}的付款。交易ID: {transaction_id}",
                "payment_failed": "付款失败: {reason}",
                "confirmation_required": "请确认您向{recipient}支付{amount} {currency}",
                "security_check_failed": "安全验证失败。请联系支持。",
                "compliance_check_failed": "需要额外验证。请提供: {documents}",
                "amount_exceeds_limit": "付款金额超过{country}的限制",
                "currency_conversion_note": "金额将从{from_currency}转换为{to_currency}",
            },
        }
