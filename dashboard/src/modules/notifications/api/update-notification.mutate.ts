import { useMutation } from "@tanstack/react-query";
import { fetch, queryClient } from "@marzneshin/common/utils";
import { toast } from "sonner";
import i18n from "@marzneshin/features/i18n";
import { NotificationsQueryFetchKey } from "./notifications.query";
import { NotificationMutationType } from "../types";


export async function updateNotification(notification: NotificationMutationType): Promise<NotificationMutationType> {
    console.log(notification)
    return fetch(`/notifications/${notification.id}`, { method: 'put', body: notification }).then((notification) => {
        return notification;
    });
}

const handleError = (error: Error, value: NotificationMutationType) => {
    toast.error(
        i18n.t('events.update.error', { name: value.label }),
        {
            description: error.message
        })
}

const handleSuccess = (value: NotificationMutationType) => {
    toast.success(
        i18n.t('events.update.success.title', { name: value.label }),
        {
            description: i18n.t('events.update.success.desc')
        })
    queryClient.invalidateQueries({ queryKey: [NotificationsQueryFetchKey] })
}


const NotificationsUpdateFetchKey = "notifications-update-fetch-key";

export const useNotificationsUpdateMutation = () => {
    return useMutation({
        mutationKey: [NotificationsUpdateFetchKey],
        mutationFn: updateNotification,
        onError: handleError,
        onSuccess: handleSuccess,
    })
}
