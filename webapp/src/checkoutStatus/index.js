import { Container, Grid, Typography } from "@mui/material";
import CheckBoxIcon from "@mui/icons-material/CheckBox";
import WarningIcon from "@mui/icons-material/Warning";

export function CheckoutStatus(props) {
  const state = props.state;
  if (!state) {
    return null;
  }

  const checkout_result = JSON.parse(state);

  if (checkout_result.success) {
    return (
      <Container sx={{ p: 4 }}>
        <Grid
          container
          direction="column"
          justifyContent="center"
          alignItems="center"
        >
          <Grid>
            <Typography variant="h6">
              <CheckBoxIcon color="success" />Check out successful
            </Typography>
          </Grid>
          <Grid>
            <Typography variant="body">Balance has been deducted</Typography>
          </Grid>
        </Grid>
      </Container>
    );
  } else {
    return (
      <Container sx={{ p: 4 }}>
        <Grid
          container
          direction="column"
          justifyContent="center"
          alignItems="center"
        >
          <Grid>
            <Typography variant="h6">
              <WarningIcon color="error" /> Check out failed
            </Typography>
          </Grid>
          <Grid>
            <Typography variant="body">
              Insufficient{" "}
              {!checkout_result.stock
                ? "stock"
                : !checkout_result.balance ? "balance" : null}
            </Typography>
          </Grid>
        </Grid>
      </Container>
    );
  }
}
