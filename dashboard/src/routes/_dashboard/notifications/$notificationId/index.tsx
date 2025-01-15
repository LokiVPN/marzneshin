import { createFileRoute, useNavigate } from '@tanstack/react-router'
import {
  useRouterNotificationContext,
  NotificationSettingsDialog,
} from '@marzneshin/modules/Notifications'
import { useDialog } from '@marzneshin/common/hooks'

const NotificationOpen = () => {
  const [settingsDialogOpen, setSettingsDialogOpen] = useDialog(true)
  const value = useRouterNotificationContext()
  const navigate = useNavigate({ from: '/notifications/$notificationId' })

  return (
    value && (
      <NotificationSettingsDialog
        open={settingsDialogOpen}
        onOpenChange={setSettingsDialogOpen}
        entity={value.notification}
        onClose={() => navigate({ to: '/notifications' })}
      />
    )
  )
}

export const Route = createFileRoute(
  '/_dashboard/notifications/$notificationId/',
)({
  component: NotificationOpen,
})
