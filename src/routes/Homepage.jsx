import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import NavigationBar from '../components/NavigationBar';

const HomePage = () => {
  
    const handleGetStartedClick = () => {
        
    };
  
    return (
        <div>
            <NavigationBar />
            <div id='intro' style={{ height: '90vh', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#FDF7ED' }}>
                <Box sx={{ textAlign: 'center', maxWidth: '600px', margin: 'auto' }}>
                <div style={{ color: '#F6A623', }}>
                    <Typography className="welcome-title" variant="h3" component="h1" gutterBottom>
                        Rewrite your health
                    </Typography>
                    <Typography variant="h5" component="h2" gutterBottom>
                        One at a time
                    </Typography>
                </div>
                <Button
                    className="button-white"
                    variant="contained"
                    color="primary"
                    sx={{ mt: 2, mr: 2, backgroundColor: '#F6A623', color: 'white', fontWeight: 600, borderRadius: '10px', padding: '5px 15px', marginLeft: '10px', '&:hover': { backgroundColor: '#e2e2e2' } }}
                    onClick={handleGetStartedClick}
                    href="/chat/mood"
                >
                    Get Started
                </Button>
                </Box>
            </div>
        </div>
    );
}
  
export default HomePage;