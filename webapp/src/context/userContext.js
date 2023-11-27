import React, { createContext, useState } from "react";
import { DEMO_USER_ID, DEMO_USER_DISPLAY_NAME } from "../util/constants";

export const UserContext = createContext();

export function UserContextProvider({ children }) {
  const [userId, setUserId] = useState(DEMO_USER_ID);
  const [userDisplayName, setUserDisplayName] = useState(
    DEMO_USER_DISPLAY_NAME
  );

  return (
    <UserContext.Provider value={{ userId, userDisplayName }}>
      {children}
    </UserContext.Provider>
  );
}
