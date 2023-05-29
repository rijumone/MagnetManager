import React from "react";

import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Tooltip from '@mui/material/Tooltip'
import TableContainer from '@mui/material/TableContainer'
import Table from '@mui/material/Table'
import TableHead from '@mui/material/TableHead'
import TableCell from '@mui/material/TableCell'
import TableRow from '@mui/material/TableRow'
import TableBody from '@mui/material/TableBody'
import Backdrop from '@mui/material/Backdrop'
import CircularProgress from '@mui/material/CircularProgress'
import Container from '@mui/material/Container'
import Stack from '@mui/material/Stack';


import ReactDOM from "react-dom/client";
import "./index.css";

class MagnetManagerApp extends React.Component {
  render() {
    // const bar = "qux"
    return (
      <>
        <SearchBox />
        {/* <Table foo={bar}/> */}
      </>
    );
  }
}

class SearchBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      loading: false,
      searchterm: '',
    };
  }
  handleSubmit = (event) => {
    event.preventDefault();
    this.setState({ ...this.state.data, loading: true }) // spread? Like python **args
    // console.log(this.input.value);
    console.log(this.state.searchterm);
    fetch("http://localhost:5400?searchterm=" + this.state.searchterm, {
    // fetch("http://localhost:5000?searchterm=" + this.input.value, {
      method: "GET",
      // body: formData
    })
      .then((response) => response.json()) // (response) => response.json() this is a function, will pass the value to the next then()
      .then((data) => this.setState({ data, loading: false }));
  };
  render() {
    return (
      <Container maxWidth="lg">
        <Stack spacing={2}>
          <form onSubmit={this.handleSubmit}>
            <Tooltip title="Enter fully or in part" arrow placement="left">
              <TextField variant="standard" label="Title or author" onChange={(e) => (this.setState({ ...this.state.data, searchterm: e.target.value }))} />
              {/* <input type="text" ref={(input) => (this.input = input)} /> */}
              {/* ref is actually like state, generally used to reference a DOM element */}
            </Tooltip>
            <Button variant="contained" type="submit">Search</Button>
            <Backdrop
              sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
              open={this.state.loading}
              // onClick={handleClose}
            >
              <CircularProgress color="inherit" />
            </Backdrop>
          </form>
          {this.state.data && (
            <TableContainer
            // component={Paper} 
            variant="outlined"
            >
                <Table aria-label="demo table">
                <TableHead><TableRow>
                <TableCell>Title</TableCell>
                <TableCell>Uploaded</TableCell>
                <TableCell>Size</TableCell>
                <TableCell>Uploader</TableCell>
                <TableCell>Magnet link</TableCell>
                </TableRow></TableHead>
                <TableBody>
                  {this.state.data.map((item) => (
                    <TableRow key={item.title}>
                      <TableCell>{item.title}</TableCell>
                      <TableCell>{item.uploaded}</TableCell>
                      <TableCell>{item.size}</TableCell>
                      <TableCell>{item.uploader}</TableCell>
                      <TableCell>
                        <a href={item.magnet_uri} rel="noreferrer" target="_blank">Add torrent</a>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Stack>
      </Container>
    );
  }
}
// ========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<MagnetManagerApp />);
