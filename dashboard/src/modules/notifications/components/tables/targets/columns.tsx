import { ColumnDef } from "@tanstack/react-table"
import { DataTableColumnHeader } from "@marzneshin/libs/entity-table"
import i18n from "@marzneshin/features/i18n"
import { NotificationTargetType, NotificationTargetSentAtPill, NotificationSkippedPill } from "@marzneshin/modules/notifications";

export const columns: ColumnDef<NotificationTargetType>[] = [
    {
        accessorKey: "user.id",
        header: ({ column }) => <DataTableColumnHeader title={i18n.t('telegram_id')} column={column} />,
    },
    {
        accessorKey: "user.username",
        header: ({ column }) => <DataTableColumnHeader title={i18n.t('username')} column={column} />,
    },
    {
        accessorKey: "sent_at",
        header: ({ column }) => (
            <DataTableColumnHeader
                title={i18n.t("sent_at")}
                column={column}
            />
        ),
        cell: ({ row }) => <NotificationTargetSentAtPill target={row.original} />,
    },
    {
        accessorKey: "skipped",
        header: ({ column }) => (
            <DataTableColumnHeader
                title={i18n.t("skipped")}
                column={column}
            />
        ),
        cell: ({ row }) => <NotificationSkippedPill target={row.original} />,
    },
];
