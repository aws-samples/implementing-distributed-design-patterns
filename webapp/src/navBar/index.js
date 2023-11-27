import React, { useContext } from "react";

import { AppBar, Grid, Typography, Toolbar } from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import { UserContext } from "../context/userContext";

export function NavBar(props) {
  const { userDisplayName } = useContext(UserContext);
  const balance = props.balance;
  return (
    <AppBar position="static" sx={{ mb: 5 }}>
      <Toolbar disableGutters>
        <Grid
          container
          direction="row"
          justifyContent="space-evenly"
          alignItems="center"
        >
          <Grid xs={3}>
            <Typography
              id="nav-bar-brand-name"
              variant="h6"
              sx={{
                fontWeight: 600,
                ml: 2
              }}
            >
              Unicorn Store
            </Typography>
          </Grid>
          <Grid
            xs={9}
            sx={{
              display: "flex",
              justifyContent: "end",
              pr: 2
            }}
          >
            <Typography
              variant="h6"
              sx={{
                pl: 2,
                pr: 1
              }}
            >
              Hi! {userDisplayName}
            </Typography>
            <Typography
              variant="h6"
              sx={{
                pl: 2
              }}
            >
              {balance
                ? <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      flexWrap: "wrap"
                    }}
                  >
                    <AccountBalanceWalletIcon />
                    <span
                      style={{
                        marginLeft: "5px"
                      }}
                    >
                      ${balance}
                    </span>
                  </div>
                : "loading..."}
            </Typography>
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
}
