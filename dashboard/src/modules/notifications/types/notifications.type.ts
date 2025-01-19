import { UserType } from "@marzneshin/modules/users";

export interface NotificationType {
    id: number;
    label: string;
    action: NotificationAction;
    message: string;
    user_ids: number[];
    created_at: string | Date;
    started_at: string | Date | null;
    finished_at: string | Date | null;
    completed: boolean;
}

export interface NotificationTargetType {
    user: UserType,
    sent_at: string | Date | null;
    skipped: boolean;
}

export interface TargetProp {
    target: NotificationTargetType;
}

export enum NotificationAction {
    USER_CREATED = "user_created",
    USER_UPDATED = "user_updated",
    USER_ACTIVATED = "user_activated",
    USER_DEACTIVATED = "user_deactivated",
    USER_DELETED = "user_deleted",
    USER_ENABLED = "user_enabled",
    USER_DISABLED = "user_disabled",
    DATA_USAGE_RESET = "data_usage_reset",
    SUBSCRIPTION_REVOKED = "subscription_revoked",
    REACHED_USAGE_PERCENT = "reached_usage_percent",
    REACHED_DAYS_LEFT = "reached_days_left",
    GET_BONUS = "get_bonus",
    CUSTOM = "custom",
}