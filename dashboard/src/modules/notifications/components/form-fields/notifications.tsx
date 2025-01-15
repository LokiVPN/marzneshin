import {
    Alert,
    AlertDescription,
    AlertTitle,
    Checkbox,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
    ScrollArea,
    Skeleton,
    Awaiting
} from "@marzneshin/common/components";
import { Link } from "@tanstack/react-router";
import { ExclamationTriangleIcon } from '@radix-ui/react-icons';
import {
    useNotificationsQuery,
    type NotificationType,
} from "@marzneshin/modules/notifications";
// import { NotificationCard } from "@marzneshin/modules/users";
import { cn } from "@marzneshin/common/utils";
import type { FC } from "react";
import {
    useFormContext,
    type FieldValues,
    type ControllerRenderProps,
} from "react-hook-form";
import { useTranslation } from "react-i18next";

interface NotificationCheckboxCardProps {
    notification: NotificationType;
    field: ControllerRenderProps<FieldValues, "notification_ids">;
}

const NotificationCheckboxCard: FC<NotificationCheckboxCardProps> = ({
    notification,
    field,
}) => (
    <div
        className={cn(
            "flex mb-2 flex-row gap-2 items-center p-3 rounded-md border",
            { "bg-secondary": field.value?.includes(notification.id) },
        )}
    >
        <Checkbox
            checked={field.value?.includes(notification.id)}
            onCheckedChange={(checked) =>
                checked
                    ? field.onChange([...field.value, notification.id])
                    : field.onChange(
                        field.value?.filter((value: number) => value !== notification.id),
                    )
            }
        />
        {/* <FormLabel className="flex flex-row justify-between items-center w-full">
            <NotificationCard notification={notification} />
        </FormLabel> */}
    </div>
);

const NotificationSkeletons: FC = () => (
    <>
        <Skeleton className="w-full h-[2.4rem]" />
        <Skeleton className="w-full h-[2.4rem]" />
        <Skeleton className="w-full h-[2.4rem]" />
    </>
);

const NotificationsList: FC<{ notifications: NotificationType[] }> = ({ notifications }) => {
    const form = useFormContext();

    return (
        <ScrollArea className="flex flex-col justify-start px-1 h-full max-h-[20rem]">
            {notifications.map((notification) => (
                <FormField
                    key={notification.id}
                    control={form.control}
                    name="notification_ids"
                    render={({ field }) => (
                        <FormItem key={notification.id}>
                            <FormControl>
                                <NotificationCheckboxCard notification={notification} field={field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            ))}
        </ScrollArea>
    );
};

const NotificationsAlert: FC = () => {
    const { t } = useTranslation();

    return (
        <Alert className="ring-1 ring-destructive-accent">
            <ExclamationTriangleIcon color="#E5484D" className="mr-2 text-destructive-accent" />
            <AlertTitle className="font-semibold text-destructive">{t('page.users.notifications-alert.title')}</AlertTitle>
            <AlertDescription>
                {t('page.users.notifications-alert.desc')}
                <Link className="m-1 font-semibold text-secondary-foreground" to="/notifications">
                    {t('page.users.notifications-alert.click')}
                </Link>
            </AlertDescription>
        </Alert>
    );
};

export const NotificationsField: FC = () => {
    const form = useFormContext();
    const { data, isFetching } = useNotificationsQuery({ page: 1, size: 100 });
    const { t } = useTranslation();

    return (
        <FormField
            control={form.control}
            name="notification_ids"
            render={() => (
                <FormItem>
                    <FormLabel>{t("notifications")}</FormLabel>
                    <Awaiting
                        isFetching={isFetching}
                        Skeleton={<NotificationSkeletons />}
                        isNotFound={data.entities.length === 0}
                        NotFound={<NotificationsAlert />}
                        Component={<NotificationsList notifications={data.entities} />}
                    />
                </FormItem>
            )}
        />
    );
};
