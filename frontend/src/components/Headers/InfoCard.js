import { Grid } from "@mui/material";
import { Card, CardBody, CardTitle } from "reactstrap";
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import { round } from "../../helper/utils";
 
const InfoCard = ({ floorPrice, volume24h, volumeAll, listCount, shock }) => {
 
   const titles = ["Floor price", "Listed count", "Volume (24h)", "Volume (All time)"]
 
   const stats = {
       "Floor price" : `◎ ${floorPrice}`,
       "Listed count" : listCount,
       "Volume (24h)" : `◎ ${volume24h}`,
       "Volume (All time)" : `◎ ${volumeAll}`,
   }
 
   const shockPercentage = {
       "Floor price" : round(shock.shock1d.floorPrice),
       "Listed count" : round(shock.shock1d.listedCount),
       "Volume (24h)" : round(shock.shock1d.volume),
       "Volume (All time)" : round(shock.shock1d.volumeAll),
   }
 
   const generateArrow = (number) => {
       if (number >= 0) {
           return <div style={{color: "rgb(132, 235, 176)", display: "flex", justifyContent: "center", alignItems: "center"}}>
               <TrendingUpIcon style={{ marginRight: "0.5vw"}}/> {number} %
           </div>
       }
       else {
           return <div style={{color: "rgb(240, 131, 131)", display: "flex", justifyContent: "center", alignItems: "center"}}>
               <TrendingDownIcon style={{ marginRight: "0.5vw"}}/> {number * -1} %
           </div>
       }
   }
 
   return (
       <Grid spacing={1} container style={{marginBottom: "10vh", marginTop: "5vh"}}>
           {titles.map(title => <Grid item xs={6}>
               <Card style={{ color: "white", backgroundColor: "#1c1f26", textAlign: "center" }}>
                   <CardBody>
                           <CardTitle
                               tag="h4"
                               className="text-uppercase text-muted mb-4"
                               style={{color: '#A8B3CF'}}
                           >
                               {title}
                           </CardTitle>
                           <div className="h5 font-weight-bold mb-3">
                               {stats[title]}
                           </div>
                           <div className="h5 font-weight-bold">
                               {generateArrow(shockPercentage[title])}
                           </div>
                   </CardBody>
               </Card>
           </Grid>)}
       </Grid>
   );
};
 
export default InfoCard;
 

