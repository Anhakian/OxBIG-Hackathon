import React from 'react'
import { AppBar, Toolbar, Typography, Button } from "@mui/material";

const NavigationBar = () => {
  return (
    <AppBar position="static" className="nav-bar" sx={{ backgroundColor:'white'}}>
            <Toolbar className="tool-bar">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                    <Typography className="logo-title" component="a" href="/" variant="h6" sx={{ textDecoration: 'none', color: '#F6A623', paddingLeft: '10px', fontWeight: 'bold', fontSize: '1.5rem'}}>
                        WellTale
                    </Typography>
                </div>
                <Button onClick={() => { window.location.href = "/chat/mood" }} color="inherit" className="button-white" sx={{ mr: 2, minWidth: '150px', backgroundColor: '#F6A623', color: 'white', fontWeight: 600, borderRadius: '10px', padding: '5px 15px 5px 15px', marginLeft: '10px', '&:hover': { backgroundColor: '#e2e2e2' } }}>
                    Get Started
                </Button>
            </Toolbar>
        </AppBar>
  )
}

export default NavigationBar