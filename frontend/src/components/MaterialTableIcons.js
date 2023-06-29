import React, { forwardRef } from "react";
import AddBox from "@material-ui/icons/AddBox";
import ArrowDownward from "@material-ui/icons/ArrowDownward";
import Check from "@material-ui/icons/Check";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import Clear from "@material-ui/icons/Clear";
import DeleteOutline from "@material-ui/icons/DeleteOutline";
import Edit from "@material-ui/icons/Edit";
import FilterList from "@material-ui/icons/FilterList";
import FirstPage from "@material-ui/icons/FirstPage";
import LastPage from "@material-ui/icons/LastPage";
import Remove from "@material-ui/icons/Remove";
import SaveAlt from "@material-ui/icons/SaveAlt";
import Search from "@material-ui/icons/Search";
import ViewColumn from "@material-ui/icons/ViewColumn";

const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} style={{color: "white"}}/>),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} style={{color: "white"}}/>),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} style={{color: "white"}}/>),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} style={{color: "white"}}/>),
  DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} style={{color: "white"}}/>),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} style={{color: "white"}}/>),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} style={{color: "white"}}/>),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} style={{color: "white"}}/>),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} style={{color: "white"}}/>),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} style={{color: "white"}}/>),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} style={{color: "white"}}/>),
  PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} style={{color: "white"}}/>),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} style={{color: "white"}}/>),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} style={{color: "white"}}/>),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} style={{color: "white"}}/>),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} style={{color: "white"}}/>),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} style={{color: "white"}}/>),
};

export default tableIcons;