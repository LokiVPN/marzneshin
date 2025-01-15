
import { DeleteConfirmation } from '@marzneshin/common/components'
import { type FC, useEffect } from 'react'
import { NotificationType, useNotificationsDeletionMutation } from '@marzneshin/modules/notifications'

interface NotificationsDeleteConfirmationDialogProps {
    onOpenChange: (state: boolean) => void
    open: boolean
    entity: NotificationType
    onClose: () => void;
}

export const NotificationsDeleteConfirmationDialog: FC<NotificationsDeleteConfirmationDialogProps> = ({ onOpenChange, open, entity, onClose }) => {
    const deleteMutation = useNotificationsDeletionMutation();
    useEffect(() => {
        if (!open) onClose();
    }, [open, onClose]);
    return (
        <DeleteConfirmation
            open={open}
            onOpenChange={onOpenChange}
            action={() => deleteMutation.mutate(entity)}
        />
    )
}
