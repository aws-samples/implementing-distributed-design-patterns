import React, { useContext, useEffect, useState } from "react";

import "./App.css";

import {
  Box,
  Button,
  ButtonGroup,
  Container,
  Grid,
  LinearProgress,
  Typography
} from "@mui/material";

import { CheckoutStatus } from "./checkoutStatus/index.js";
import { NavBar } from "./navBar/index.js";
import {
  // PointsAPIVersionSwitch,
  UnicornPointsSummary
} from "./points/index.js";
import { Product } from "./products/index.js";
import { Campaign } from "./campaigns/index.js";
import {
  getCampaigns,
  getProduct,
  getUserBalance,
  getUserPointsSummaryDaily
} from "./util/api.js";
import { UserContext } from "./context/userContext";

function App() {
  const { userId } = useContext(UserContext);
  const [userBalance, setUserBalance] = useState(null);
  const retailPage = "retailPage";
  const pointsPage = "pointsPage";
  const campaignPage = "campaignPage";

  const [refreshData, setRefreshData] = useState(0);
  const [displayPage, setDisplayPage] = useState(retailPage);

  useEffect(
    () => {
      async function fetchData() {
        const userBalance = await getUserBalance(userId);
        setUserBalance(userBalance.balance);
      }
      fetchData();
    },
    [refreshData, userId]
  );
  return (
    <React.Fragment>
      <NavBar balance={userBalance} />
      <ButtonGroup
        variant="outlined"
        aria-label="page switch group"
        sx={{
          display: "flex",
          margin: "0 auto",
          width: "fit-content",
          mb: 5
        }}
      >
        <Button
          variant={displayPage === retailPage ? "contained" : "outlined"}
          onClick={() => {
            setDisplayPage(retailPage);
          }}
        >
          Buy Unicorns
        </Button>
        <Button
          variant={displayPage === pointsPage ? "contained" : "outlined"}
          onClick={() => {
            setDisplayPage(pointsPage);
          }}
        >
          Points Center
        </Button>
        <Button
          variant={displayPage === campaignPage ? "contained" : "outlined"}
          onClick={() => {
            setDisplayPage(campaignPage);
          }}
        >
          Campaign Center
        </Button>
      </ButtonGroup>
      <Container
        sx={{
          width: "80%",
          minWidth: 300
        }}
      >
        {(displayPage === retailPage &&
          <RetailPage setRefreshData={setRefreshData} />) ||
          (displayPage === pointsPage && <PointsPage />) ||
          (displayPage === campaignPage && <CampaignPage />)}
      </Container>
    </React.Fragment>
  );
}

function RetailPage(props) {
  const productId = 1;
  const [product, setProduct] = useState(null);
  const [checkoutState, setCheckoutState] = useState(null);

  useEffect(
    () => {
      async function fetchData() {
        const productInfo = await getProduct(productId);
        setProduct(productInfo);
      }
      fetchData();
    },
    [checkoutState]
  );

  return (
    <React.Fragment>
      <Grid container id="product-container">
        <Grid xs={12}>
          {product
            ? <Product
                product={product}
                setCheckoutState={setCheckoutState}
                setRefreshData={props.setRefreshData}
              />
            : <Typography>Loading...</Typography>}
        </Grid>
        <Grid item xs={12}>
          <CheckoutStatus state={checkoutState} />
        </Grid>
      </Grid>
    </React.Fragment>
  );
}

function PointsPage(props) {
  const { userId } = useContext(UserContext);
  const [pointsAPIVersion, setPointsAPIVersion] = useState("cqrs");
  const [pointsSummary, setPointsSummary] = useState([]);
  const [isPointsDataLoaded, setIsPointsDataLoaded] = useState(false);
  useEffect(() => {
    async function fetchData() {
      const userPointsSummary = await getUserPointsSummaryDaily(
        userId,
        pointsAPIVersion
      );
      setPointsSummary(userPointsSummary);
      setIsPointsDataLoaded(true);
    }
    fetchData();
  }, []);
  return (
    <React.Fragment>
      <Grid
        container
        id="points-container"
        direction="column"
        justifyContent="center"
        alignItems="center"
      >
        <Grid item sx={{ width: "fit-content" }}>
          {/* <PointsAPIVersionSwitch
            APIVersion={pointsAPIVersion}
            setAPIVersion={setPointsAPIVersion}
          /> */}
        </Grid>
        <Grid item sx={{ width: "fit-content" }}>
          {isPointsDataLoaded
            ? <UnicornPointsSummary pointsSummary={pointsSummary} />
            : <Box sx={{ width: "100%" }}>
                <Typography>Loading...</Typography>
                <LinearProgress />
              </Box>}
        </Grid>
      </Grid>
    </React.Fragment>
  );
}

function CampaignPage(props) {
  const [campaigns, setCampaigns] = useState(null);
  const [isCampaignDataDataLoaded, setIsCampaignDataLoaded] = useState(false);

  useEffect(() => {
    async function fetchData() {
      const campaign = await getCampaigns();
      setCampaigns(campaign);
      setIsCampaignDataLoaded(true);
    }
    fetchData();
  }, []);

  return (
    <React.Fragment>
      <Grid
        container
        id="campaign-container"
        direction="column"
        justifyContent="center"
        alignItems="center"
      >
        <Grid item sx={{ width: "fit-content" }}>
          {isCampaignDataDataLoaded
            ? <Campaign campaignData={campaigns} />
            : <Box sx={{ width: "100%" }}>
                <Typography>Loading...</Typography>
                <LinearProgress />
              </Box>}
        </Grid>
      </Grid>
    </React.Fragment>
  );
}

export default App;
