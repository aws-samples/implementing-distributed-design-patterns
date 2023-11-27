import React from "react";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";

import {
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from "@mui/material";

export function Campaign(props) {
  return (
    <React.Fragment>
      <Grid container direction="column" alignItems="flexS
      ">
        <Grid item>
          <Typography variant="h5">Campaigns</Typography>
        </Grid>
        <Grid item>
          <Typography>
            A daily summary of the net amount of points issued/deducted from
            your account
          </Typography>
        </Grid>
        <CampaignTable campaignData={props.campaignData} />
      </Grid>
    </React.Fragment>
  );
}

const handleChange = json => {
  // You can implement logic to update the campaign rule logic here
};

function CampaignTable(props) {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 300 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Client</TableCell>
            <TableCell align="center">Campaign</TableCell>
            <TableCell align="center">Rules</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.campaignData.items.map(item =>
            <TableRow
              key={`${item.client}-${item.campaign_name}`}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {item.client}
              </TableCell>
              <TableCell align="left">
                {item.campaign_name}
              </TableCell>
              <TableCell align="left">
                <CodeMirror
                  id={`${item.client}-${item.campaign_name}`}
                  value={JSON.stringify(JSON.parse(item.rules), null, 2)}
                  theme={"dark"}
                  basicSetup={{ lineNumbers: true }}
                  height="200px"
                  width="auto"
                  onChange={handleChange}
                  extensions={[json()]}
                />
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
