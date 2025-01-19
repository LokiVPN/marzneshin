
import { FC } from "react";
import { DoubleEntityTable } from "@marzneshin/libs/entity-table";
import { columns } from "./columns";
import { fetchNotificationUsers, type NotificationType } from "@marzneshin/modules/notifications";

interface NotificationTargetsTableProps {
    notification: NotificationType
}

export const NotificationTargetsTable: FC<NotificationTargetsTableProps> = ({ notification }) => {

    return (
        <DoubleEntityTable
            columns={columns}
            entityId={notification.id}
            fetchEntity={fetchNotificationUsers}
            primaryFilter="user.id"
            entityKey='notification-targets'
        />
    )
}
