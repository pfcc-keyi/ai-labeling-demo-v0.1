import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Textarea,
  VStack,
  HStack,
  Heading,
  Alert,
  AlertIcon,
  Card,
  CardBody,
  CardHeader,
  Text,
  Badge,
  Select,
  Spinner,
  useToast,
  Divider,
  ButtonGroup,
} from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import { labelText, submitFeedback, getStatus, getLabels } from '../utils/api';
import { getAccountId, logout } from '../utils/auth';

interface LabelingInterfaceProps {
  onLogout: () => void;
}

const LabelingInterface = ({ onLogout }) => {
  const [inputText, setInputText] = useState('');
  const [modelName, setModelName] = useState('gpt-4');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [correctedLabel, setCorrectedLabel] = useState('');
  const [availableLabels, setAvailableLabels] = useState([]);
  const [systemStatus, setSystemStatus] = useState(null);
  const [statusLoading, setStatusLoading] = useState(false);
  
  const toast = useToast();
  const accountId = getAccountId();

  // Check system status periodically
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const status = await getStatus();
        setSystemStatus(status);
      } catch (error) {
        console.error('Failed to fetch status:', error);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 5000); // Check every 5 seconds
    return () => clearInterval(interval);
  }, []);

  // Load available labels
  useEffect(() => {
    const fetchLabels = async () => {
      try {
        const response = await getLabels();
        setAvailableLabels(response.labels);
      } catch (error) {
        console.error('Failed to fetch labels:', error);
      }
    };
    fetchLabels();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter some text to label',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    setLoading(true);
    setResult(null);
    setShowFeedback(false);

    try {
      const response = await labelText({
        text: inputText,
        model_name: modelName,
      });
      setResult(response);
      setShowFeedback(true);
    } catch (error) {
      if (error.response?.status === 423) {
        toast({
          title: 'System Busy',
          description: error.response.data.detail,
          status: 'warning',
          duration: 5000,
        });
      } else {
        toast({
          title: 'Error',
          description: error.response?.data?.detail || 'Failed to label text',
          status: 'error',
          duration: 5000,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (isSupported) => {
    if (!result) return;

    setFeedbackLoading(true);
    try {
      await submitFeedback({
        request_id: result.id,
        is_supported: isSupported,
        corrected_label: isSupported ? undefined : correctedLabel,
      });

      toast({
        title: 'Success',
        description: 'Feedback submitted successfully',
        status: 'success',
        duration: 3000,
      });
      setShowFeedback(false);
      setInputText('');
      setResult(null);
      setCorrectedLabel('');
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to submit feedback',
        status: 'error',
        duration: 3000,
      });
    } finally {
      setFeedbackLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    onLogout();
  };

  return (
    <Box minH="100vh" bg="gray.50" p={6}>
      <VStack spacing={6} maxW="4xl" mx="auto">
        {/* Header */}
        <HStack justify="space-between" w="full">
          <Heading size="lg">AI Labeling Platform</Heading>
          <HStack>
            <Text fontSize="sm" color="gray.600">
              Welcome, {accountId}
            </Text>
            <Button size="sm" onClick={handleLogout}>
              Logout
            </Button>
          </HStack>
        </HStack>

        {/* System Status */}
        {systemStatus && (
          <Card w="full">
            <CardBody>
              <HStack justify="space-between">
                <Text fontWeight="medium">System Status:</Text>
                <Badge colorScheme={systemStatus.is_busy ? 'red' : 'green'}>
                  {systemStatus.is_busy ? 'Busy' : 'Available'}
                </Badge>
              </HStack>
              {systemStatus.is_busy && (
                <Text fontSize="sm" color="gray.600" mt={2}>
                  User "{systemStatus.current_user}" is currently processing a request...
                </Text>
              )}
            </CardBody>
          </Card>
        )}

        {/* Main Form */}
        <Card w="full">
          <CardHeader>
            <Heading size="md">Text Classification</Heading>
          </CardHeader>
          <CardBody>
            <form onSubmit={handleSubmit}>
              <VStack spacing={4}>
                <FormControl>
                  <FormLabel>Model Selection</FormLabel>
                  <HStack>
                    <Button
                      size="sm"
                      colorScheme={modelName === 'gpt-4' ? 'blue' : 'gray'}
                      onClick={() => setModelName('gpt-4')}
                    >
                      GPT-4
                    </Button>
                    <Button
                      size="sm"
                      colorScheme={modelName === 'gpt-3.5-turbo' ? 'blue' : 'gray'}
                      onClick={() => setModelName('gpt-3.5-turbo')}
                    >
                      GPT-3.5 Turbo
                    </Button>
                  </HStack>
                </FormControl>

                <FormControl>
                  <FormLabel>Text to Label</FormLabel>
                  <Textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Enter the job description or financial services experience text..."
                    rows={8}
                  />
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="blue"
                  size="lg"
                  w="full"
                  isLoading={loading}
                  loadingText="Processing..."
                  isDisabled={systemStatus?.is_busy}
                >
                  {systemStatus?.is_busy ? 'System Busy - Please Wait' : 'Label Text'}
                </Button>
              </VStack>
            </form>
          </CardBody>
        </Card>

        {/* Results */}
        {result && (
          <Card w="full">
            <CardHeader>
              <Heading size="md">Results</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <Box>
                  <Text fontWeight="medium" mb={2}>Input Text:</Text>
                  <Text fontSize="sm" bg="gray.100" p={3} borderRadius="md">
                    {result.input_text}
                  </Text>
                </Box>

                <Box>
                  <Text fontWeight="medium" mb={2}>Model Used:</Text>
                  <Badge colorScheme="blue">{result.model_name}</Badge>
                </Box>

                <Box>
                  <Text fontWeight="medium" mb={2}>Predicted Label:</Text>
                  {result.predicted_label ? (
                    <Badge colorScheme="green" fontSize="sm" p={2}>
                      {result.predicted_label}
                    </Badge>
                  ) : (
                    <Text color="red.500">No label predicted</Text>
                  )}
                </Box>

                <Box>
                  <Text fontWeight="medium" mb={2}>Processing Time:</Text>
                  <Text fontSize="sm">{result.processing_time.toFixed(2)} seconds</Text>
                </Box>

                {result.error_message && (
                  <Alert status="error">
                    <AlertIcon />
                    {result.error_message}
                  </Alert>
                )}

                {/* Feedback Section */}
                {showFeedback && result.predicted_label && (
                  <>
                    <Divider />
                    <Box>
                      <Text fontWeight="medium" mb={3}>
                        Do you support this result?
                      </Text>
                      <ButtonGroup spacing={4}>
                        <Button
                          colorScheme="green"
                          onClick={() => handleFeedback(true)}
                          isLoading={feedbackLoading}
                        >
                          ✓ Support
                        </Button>
                        <Button
                          colorScheme="red"
                          onClick={() => setShowFeedback('reject')}
                        >
                          ✗ Don't Support
                        </Button>
                      </ButtonGroup>

                      {showFeedback === 'reject' && (
                        <Box mt={4}>
                          <FormControl>
                            <FormLabel>Select the correct label:</FormLabel>
                            <Select
                              value={correctedLabel}
                              onChange={(e) => setCorrectedLabel(e.target.value)}
                              placeholder="Choose the correct label..."
                            >
                              {availableLabels.map((label) => (
                                <option key={label} value={label}>
                                  {label}
                                </option>
                              ))}
                            </Select>
                          </FormControl>
                          <HStack mt={3}>
                            <Button
                              colorScheme="blue"
                              onClick={() => handleFeedback(false)}
                              isLoading={feedbackLoading}
                              isDisabled={!correctedLabel}
                            >
                              Submit Correction
                            </Button>
                            <Button onClick={() => setShowFeedback(true)}>
                              Cancel
                            </Button>
                          </HStack>
                        </Box>
                      )}
                    </Box>
                  </>
                )}
              </VStack>
            </CardBody>
          </Card>
        )}
      </VStack>
    </Box>
  );
};

export default LabelingInterface; 