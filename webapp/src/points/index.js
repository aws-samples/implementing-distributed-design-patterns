import React, { useContext } from "react";

import {
  Grid,
  Paper,
  Radio,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel
} from "@mui/material";

import { UserContext } from "../context/userContext";

export function UnicornPointsSummary(props) {
  const { userDisplayName } = useContext(UserContext);
  return (
    <React.Fragment>
      <Grid
        container
        direction="column"
        alignItems="flex"
        sx={{ width: "fit-content" }}
      >
        <Grid item>
          <Typography variant="h5">
            Unicorn Points Summary for: {userDisplayName}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant="subtitle1">
            A daily summary of the points value changes from your account
          </Typography>
        </Grid>
        <PointsTotalDisplay pointsBalance={props.pointsSummary.balance} />
        <PointsDailySummaryTable pointsSummary={props.pointsSummary} />
      </Grid>
    </React.Fragment>
  );
}

export function PointsAPIVersionSwitch(props) {
  /* 
  This is where you can implement the naive implementation with 
  a single relational database and compare the speed difference
  */
  const handleChange = event => {
    props.setAPIVersion(event.target.value);
  };
  return (
    <React.Fragment>
      <FormControl sx={{ mb: 4, minWidth: 460 }}>
        <FormLabel id="controlled-radio-buttons-group">API Version</FormLabel>
        <RadioGroup
          aria-labelledby="controlled-radio-buttons-group"
          name="controlled-radio-buttons-group"
          value={props.APIVersion}
          onChange={handleChange}
        >
          <FormControlLabel
            value="naive"
            control={<Radio />}
            label="Naive Implementation"
          />
          <FormControlLabel value="cqrs" control={<Radio />} label="CQRS" />
        </RadioGroup>
      </FormControl>
    </React.Fragment>
  );
}

function PointsDailySummaryTable(props) {
  return (
    <TableContainer component={Paper} sx={{ mt: 2, maxWidth: 400 }}>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Date DD/MM/YYYY</TableCell>
            <TableCell align="right">Account</TableCell>
            <TableCell align="right">Points Issued</TableCell>
            <TableCell align="right">Points Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.pointsSummary.balance_entries.map(row =>
            <TableRow
              key={row.issued_date}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              style={
                row.status === "expired"
                  ? { backgroundColor: "#EEEEEE" }
                  : { backgroundColor: "#FFFFFF" }
              }
            >
              <TableCell component="th" scope="row">
                {row.issued_date}
              </TableCell>
              <TableCell align="right">
                {props.pointsSummary.account_id}
              </TableCell>
              <TableCell align="right">
                {row.balance}
              </TableCell>
              <TableCell align="right">
                {row.status}
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

function PointsTotalDisplay(props) {
  return (
    <Typography variant="h6" sx={{ mt: 3 }}>
      Available Balance: <b>{props.pointsBalance}</b>
    </Typography>
  );
}
