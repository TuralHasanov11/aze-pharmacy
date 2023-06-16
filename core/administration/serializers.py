from abc import ABC
from datetime import datetime

from django.utils import translation
from django.utils.translation import gettext_lazy as _
from simple_history.utils import update_change_reason


class LogSerializer(ABC):
    fields: dict

    def __init__(self, instance, logs):
        self.logs = logs
        self.instance = instance
        self.data = []
        for log in self.logs:
            changes = self.compareChanges(log)
            if changes:
                log.changes = changes
            self.data.append(log)

    def compareChanges(self, log):
        if log.prev_record:
            return log.diff_against(log.prev_record).changes
        return None

    def save(self):
        translation.activate("az")
        log = self.logs[0]
        print(log.history_user)
        result = ""
        try:
            if hasattr(log, 'changes'):
                log.history_change_reason = ""
                for change in log.changes:
                    if change.field in self.fields:
                        result += f"{self.fields[change.field]} dəyişdirildi.\n"
                log.history_change_reason = result
                update_change_reason(self.instance, result)
            log.history_date = datetime.fromisoformat(
                str(log.history_date)).strftime("%d.%m.%Y %H:%M")
            return self.serialize(log)
        except Exception:
            return self.serialize(log)

    def serialize(self, log):
        return {
            "history_user": str(log.history_user),
            "history_date": log.history_date,
            "history_change_reason": log.history_change_reason,
            "history_id": log.history_id,
            "history_type": log.history_type,
        }


class OrderLogSerializer(LogSerializer):
    fields: dict = {
        "notes": _("Notes")
    }


class OrderDeliveryLogSerializer(LogSerializer):
    fields: dict = {
        "delivery_status": _("Delivery Status"),
        "delivery_date": _("Delivery Date"),
        "courier_name": _("Courier Name"),
        "tracking_number": _("Tracking Number"),
    }
