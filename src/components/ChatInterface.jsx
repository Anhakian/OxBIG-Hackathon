import { Box, Button, Stack, TextField } from '@mui/material';
import NavigationBar from './NavigationBar';

const ChatInterface = ({ 
    messages, 
    message, 
    setMessage, 
    sendMessage, 
    isLoading, 
    disabled 
}) => {
    const handleSubmit = (e) => {
        e.preventDefault();
        sendMessage();
    };

    return (
        <div>
            <NavigationBar />
            <Box 
                height="90vh" 
                display="flex" 
                flexDirection="column" 
                justifyContent="center" 
                alignItems="center"
                style={{ backgroundColor: '#FDF7ED' }}
            >
                <Stack 
                    direction="column" 
                    width="900px" 
                    height="500px" 
                    border="1px solid black" 
                    p={2} 
                    spacing={3}
                    style={{ backgroundColor: '#FDF7ED', borderRadius: '10px', borderColor: '#F6A623' }}
                >
                    <Stack 
                        direction="column" 
                        spacing={2} 
                        flexGrow={1} 
                        overflow="auto" 
                        maxHeight="100%"
                        sx={{
                            '&::-webkit-scrollbar': {
                                width: '8px',
                            },
                            '&::-webkit-scrollbar-track': {
                                background: '#f1f1f1',
                            },
                            '&::-webkit-scrollbar-thumb': {
                                background: '#888',
                                borderRadius: '4px',
                            },
                        }}
                    >
                        {messages.map((message, index) => (
                            <Box 
                                key={index} 
                                display="flex" 
                                flexDirection="row" 
                                justifyContent={message.role === "assistant" ? "flex-start" : "flex-end"}
                            >
                                <Box 
                                    bgcolor={message.role === "assistant" ? "#F8BFBF" : "#F6A623"} 
                                    color="white" 
                                    borderRadius={10} 
                                    p={2}
                                    maxWidth="80%"
                                    sx={{
                                        wordBreak: 'break-word'
                                    }}
                                >
                                    {message.content}
                                    {message.imageUrl && (
                                        <Box mt={2}>
                                            <img src={message.imageUrl} alt="Generated content" style={{ maxWidth: '100%', borderRadius: '8px' }} />
                                        </Box>
                                    )}
                                </Box>
                            </Box>
                        ))}
                    </Stack>
                    <form onSubmit={handleSubmit} style={{ width: '100%' }}>
                        <Stack width="100%" direction="row" spacing={2}>
                            <TextField 
                                fullWidth 
                                label="Message" 
                                value={message} 
                                onChange={(e) => setMessage(e.target.value)}
                                disabled={disabled || isLoading}
                                style={{ backgroundColor: '#F8BFBF', borderRadius: '5px' }}
                            />
                            <Button 
                                variant="contained" 
                                onClick={sendMessage}
                                disabled={disabled || isLoading}
                                style={{ backgroundColor: '#F6A623', borderRadius: '5px' }}
                            >
                                Send
                            </Button>
                        </Stack>
                    </form>
                </Stack>
            </Box>
            
        </div>
    );
};

export default ChatInterface;