import { createFileRoute, useNavigate } from '@tanstack/react-router'
import {
  NotificationsDeleteConfirmationDialog,
  useRouterNotificationContext,
} from '@marzneshin/modules/notifications'
import { useDialog } from '@marzneshin/common/hooks'

const NotificationDelete = () => {
  const [deleteDialogOpen, setDeleteDialogOpen] = useDialog(true)
  const value = useRouterNotificationContext()
  const navigate = useNavigate({ from: '/notifications/$notificationId/delete' })

  return (
    value && (
      <NotificationsDeleteConfirmationDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        entity={value.notification}
        onClose={() => navigate({ to: '/notifications' })}
      />
    )
  )
}

export const Route = createFileRoute(
  '/_dashboard/notifications/$notificationId/delete',
)({
  component: NotificationDelete,
})
