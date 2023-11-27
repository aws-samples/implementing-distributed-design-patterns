import React, { useContext, useState } from "react";

import {
  Alert,
  Grid,
  Typography,
  Button,
  Card,
  CardHeader,
  CardMedia,
  CardContent,
  CardActions,
  CircularProgress,
  TextField
} from "@mui/material";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import { UserContext } from "../context/userContext";
import { triggerStepFunction } from "../util/api";

export function Product(props) {
  const { userId } = useContext(UserContext);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [quantity, setQuantity] = useState(1);

  const product = props.product;
  return (
    <Card sx={{ padding: 2, maxWidth: 600, margin: "0 auto" }}>
      <CardHeader
        title={product.name}
        subheader={`In stock: ${product.stock}`}
      />
      <CardMedia
        component="img"
        image={product.image}
        alt={product.name}
        sx={{
          maxWidth: 300,
          margin: "0 auto"
        }}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {product.description}
        </Typography>
        <Alert severity="info" sx={{ mt: 2 }}>
          <Typography>
            Earn <b>Unicorn Points</b> with this purchase! $10 = 1 Unicorn
            Points!
          </Typography>
        </Alert>
      </CardContent>

      <CardActions disableSpacing>
        <Grid
          container
          direction="row"
          justifyContent="space-between"
          alignItems="flex-end"
        >
          <Grid>
            <Typography variant="h5" color="text.secondary">
              ${product.price}
            </Typography>
          </Grid>
          <Grid>
            {isSubmitting
              ? <CircularProgress />
              : <React.Fragment>
                  <TextField
                    value={quantity}
                    type="number"
                    placeholder="1"
                    size="small"
                    label="Quantity"
                    sx={{
                      width: 100
                    }}
                    onChange={event => {
                      setQuantity(event.target.value);
                    }}
                  />
                  <Button
                    disabled={isSubmitting || quantity === 0}
                    variant="contained"
                    onClick={async () => {
                      const timeStamp = new Date();
                      setIsSubmitting(true);
                      const state = await triggerStepFunction(
                        userId,
                        product.id,
                        quantity
                      );
                      props.setCheckoutState(state.output);
                      props.setRefreshData(timeStamp);
                      setIsSubmitting(false);
                    }}
                    sx={{ ml: 1 }}
                    startIcon={<AccountBalanceWalletIcon />}
                  >
                    Quick Buy
                  </Button>
                </React.Fragment>}
          </Grid>
        </Grid>
      </CardActions>
    </Card>
  );
}
