import { useMutation } from "@tanstack/react-query";
import { fetch, queryClient } from "@marzneshin/common/utils";
import { toast } from "sonner";
import i18n from "@marzneshin/features/i18n";
import {
    NotificationMutationType
} from "@marzneshin/modules/notifications";

export async function notificationStart(notification: NotificationMutationType): Promise<NotificationMutationType> {
    return fetch(`/notifications/${notification.id}/start`, { method: 'post', body: notification }).then((user) => {
        return user;
    });
}

const handleError = (error: Error, value: NotificationMutationType) => {
    toast.error(
        i18n.t('events.notification_start.error', { name: value.label }),
        {
            description: error.message
        })
}

const handleSuccess = (value: NotificationMutationType) => {
    toast.success(
        i18n.t('events.notification_start.success.title', { name: value.label }),
        {
            description: i18n.t('events.notification_start.success.desc')
        })
    queryClient.invalidateQueries({ queryKey: [NotificationsStartFetchKey] })
}


const NotificationsStartFetchKey = "notification-start-fetch-key";

export const useNotificationStartCmd = () => {
    return useMutation({
        mutationKey: [NotificationsStartFetchKey, "start"],
        mutationFn: notificationStart,
        onError: handleError,
        onSuccess: handleSuccess,
    })
}