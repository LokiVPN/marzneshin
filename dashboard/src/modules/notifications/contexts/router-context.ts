import { createContext, useContext } from "react";
import { NotificationType } from "@marzneshin/modules/notifications";

interface RouterNotificationContextProps {
    notification: NotificationType;
}

export const RouterNotificationContext = createContext<RouterNotificationContextProps | null>(null);

export const useRouterNotificationContext = () => {
    const ctx = useContext(RouterNotificationContext);
    return ctx;
};
