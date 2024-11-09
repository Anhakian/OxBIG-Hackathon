import React from 'react'
import { AppBar, Toolbar, Typography } from "@mui/material";

const NavigationBar = () => {
  return (
    <AppBar position="static" className="nav-bar" sx={{ backgroundColor:'white'}}>
            <Toolbar className="tool-bar">
                <div style={{ display: 'flex', alignItems: 'center'}}>
                    <Typography className="logo-title" component="a" href="/" variant="h6" sx={{  textDecoration: 'none', color: 'black', paddingLeft: '10px', fontWeight: 'bold'}}>
                        WellTale
                    </Typography>
                </div>
                
            </Toolbar>
        </AppBar>
  )
}

export default NavigationBar