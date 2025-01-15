import { useMutation } from "@tanstack/react-query";
import { fetch, queryClient } from "@marzneshin/common/utils";
import { toast } from "sonner";
import i18n from "@marzneshin/features/i18n";
import {
    NotificationMutationType
} from "@marzneshin/modules/notifications";

export async function notificationTest(notification: NotificationMutationType): Promise<NotificationMutationType> {
    return fetch(`/notifications/${notification.id}/test`, { method: 'post', body: notification }).then((user) => {
        return user;
    });
}

const handleError = (error: Error, value: NotificationMutationType) => {
    toast.error(
        i18n.t('events.notification_test.error', { name: value.label }),
        {
            description: error.message
        })
}

const handleSuccess = (value: NotificationMutationType) => {
    toast.success(
        i18n.t('events.notification_test.success.title', { name: value.label }),
        {
            description: i18n.t('events.notification_test.success.desc')
        })
    queryClient.invalidateQueries({ queryKey: [NotificationsTestFetchKey] })
}


const NotificationsTestFetchKey = "notification-test-fetch-key";

export const useNotificationTestCmd = () => {
    return useMutation({
        mutationKey: [NotificationsTestFetchKey, "test"],
        mutationFn: notificationTest,
        onError: handleError,
        onSuccess: handleSuccess,
    })
}