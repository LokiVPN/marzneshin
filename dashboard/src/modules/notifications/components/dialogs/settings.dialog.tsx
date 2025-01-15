import {
  SettingsDialogProps,
  SettingsDialog,
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Button
} from "@marzneshin/common/components";
import { FC, useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  NotificationsUsersTable,
  NotificationDetailTable,
  NotificationType,
  useNotificationTestCmd,
  useNotificationStartCmd
} from "@marzneshin/modules/notifications";
import { SendIcon, PlayIcon } from "lucide-react";

interface NotificationSettingsDialogProps extends SettingsDialogProps {
  entity: NotificationType;
  onClose: () => void;
}

export const NotificationSettingsDialog: FC<NotificationSettingsDialogProps> = ({
  onOpenChange,
  open,
  entity,
  onClose,
}) => {
  const { mutate: testNotification } = useNotificationTestCmd();
  const { mutate: startNotification } = useNotificationStartCmd();
  const { t } = useTranslation();

  return (
    <SettingsDialog open={open} onClose={onClose} onOpenChange={onOpenChange}>
      <Card>
            <CardHeader className="flex flex-row justify-between items-center w-full">
                <CardTitle>{t("notification_info")}</CardTitle>
                <div className="hstack justify-center items-center gap-2">
                    <Button
                        className={"bg-warning rounded-2xl"}
                        onClick={() => testNotification(entity)}
                    >
                        <SendIcon />
                    </Button>
                    <Button
                        className="bg-success rounded-2xl"
                        onClick={() => startNotification(entity)}
                    >
                        <PlayIcon />
                    </Button>
                </div>
            </CardHeader>
            <CardContent>
              <Tabs className="my-3 w-full h-full" defaultValue="info">
                <TabsList className="w-full">
                  <TabsTrigger className="w-full" value="info">
                    {t("info")}
                  </TabsTrigger>
                  <TabsTrigger className="w-full" value="users">
                    {t("users")}
                  </TabsTrigger>
                </TabsList>
                <TabsContent value="info" className="h-full">
                  <NotificationDetailTable notification={entity} />
                </TabsContent>
                <TabsContent value="users" className="h-full">
                  <NotificationsUsersTable notification={entity} />
                </TabsContent>
              </Tabs>
            </CardContent>
        </Card>


      
    </SettingsDialog>
  );
};
