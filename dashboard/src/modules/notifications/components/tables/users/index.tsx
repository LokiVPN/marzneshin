
import { FC } from "react";
import { DoubleEntityTable } from "@marzneshin/libs/entity-table";
import { columns } from "./columns";
import { fetchNotificationUsers, type NotificationType } from "@marzneshin/modules/notifications";

interface NotificationsUsersTableProps {
    notification: NotificationType
}

export const NotificationsUsersTable: FC<NotificationsUsersTableProps> = ({ notification }) => {

    return (
        <DoubleEntityTable
            columns={columns}
            entityId={notification.id}
            fetchEntity={fetchNotificationUsers}
            primaryFilter="label"
            entityKey='notifications'
        />
    )
}
