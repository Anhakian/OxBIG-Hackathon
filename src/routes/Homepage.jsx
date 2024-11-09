import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import NavigationBar from '../components/NavigationBar';

const HomePage = () => {
  
    const handleGetStartedClick = () => {
        
    };
  
    return (
        <div>
            <NavigationBar />
            <div id='intro' style={{ height: '80vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <Box sx={{ textAlign: 'center', maxWidth: '600px', margin: 'auto' }}>
                <div>
                    <Typography className="welcome-title" variant="h3" component="h1" gutterBottom>
                        WellTale
                    </Typography>
                    <Typography variant="h5" component="h2" gutterBottom>
                    A Journey Through Your Mind
                    </Typography>
                </div>
                <Button
                    className="button-white"
                    variant="contained"
                    color="primary"
                    sx={{ mt: 2, mr: 2, backgroundColor: 'white', color: 'black', fontWeight: 600, borderRadius: '10px', padding: '5px 15px', marginLeft: '10px', '&:hover': { backgroundColor: '#e2e2e2' } }}
                    onClick={handleGetStartedClick}
                >
                    Get Started
                </Button>
                <Button
                    className="button-blue"
                    variant="outlined"
                    color="primary"
                    sx={{ mt: 2, backgroundColor: '#2E46CD', color: 'white', fontWeight: 600, borderRadius: '10px', padding: '5px 15px', marginLeft: '10px', '&:hover': { backgroundColor: '#1565C0' } }}
                >
                    Learn More
                </Button>
                </Box>
            </div>
        </div>
    );
}
  
export default HomePage;