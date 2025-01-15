import { createFileRoute, defer, Await, Outlet } from '@tanstack/react-router'
import {
  RouterNotificationContext,
  fetchNotification,
} from '@marzneshin/modules/notifications'
import { Suspense } from 'react'
import {
  AlertDialog,
  AlertDialogContent,
  Loading,
} from '@marzneshin/common/components'

const NotificationProvider = () => {
  const { notification } = Route.useLoaderData()
  return (
    <Suspense fallback={<Loading />}>
      <Await promise={notification}>
        {(notification) => (
          <RouterNotificationContext.Provider value={{ notification }}>
            <Suspense>
              <Outlet />
            </Suspense>
          </RouterNotificationContext.Provider>
        )}
      </Await>
    </Suspense>
  )
}

export const Route = createFileRoute(
  '/_dashboard/notifications/$notificationId',
)({
  loader: async ({ params }) => {
    const notificationPromise = fetchNotification({
      queryKey: ['notifications', Number.parseInt(params.notificationId)],
    })

    return {
      notification: defer(notificationPromise),
    }
  },
  errorComponent: () => (
    <AlertDialog open={true}>
      <AlertDialogContent>Notification not found</AlertDialogContent>
    </AlertDialog>
  ),
  component: NotificationProvider,
})
