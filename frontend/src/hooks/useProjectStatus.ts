import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';
const POLLING_INTERVAL = 3000; // Poll every 3 seconds

export const useProjectStatus = (runId: string | null) => {
    const [agentState, setAgentState] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [isPolling, setIsPolling] = useState<boolean>(false);

    useEffect(() => {
        let intervalId: NodeJS.Timeout | null = null;

        if (runId) {
            setIsPolling(true);
            
            const fetchStatus = async () => {
                try {
                    const response = await axios.get(`${API_BASE_URL}/project/${runId}/status`);
                    const lastNodeState = response.data[Object.keys(response.data)[0]]; // Get the inner state object
                    setAgentState(lastNodeState);

                    // Stop polling if the agent reaches a terminal state
                    if (lastNodeState.last_completed_step === 'step_17_reengage_workflow' || lastNodeState.last_completed_step === 'END') {
                        setIsPolling(false);
                    }
                } catch (err) {
                    console.error("Error fetching project status:", err);
                    setError("Could not retrieve project status.");
                    setIsPolling(false);
                }
            };
            
            // Fetch immediately on new runId, then start polling
            fetchStatus();
            intervalId = setInterval(fetchStatus, POLLING_INTERVAL);
        } else {
            setIsPolling(false);
        }

        // Cleanup function: clear interval when the component unmounts or runId changes
        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };

    }, [runId]);

    return { agentState, error, isPolling };
};