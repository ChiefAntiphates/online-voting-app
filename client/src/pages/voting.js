import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";
import { useLocation, useParams } from 'react-router-dom';
import { SOCKET_BASE } from "../Constants";

const Voting = props => {
    const uid = useParams().id
    const [currentRoundId, setCurrentRoundId] = useState()
    const [currentRound, setCurrentRound] = useState([])
    const [candidates, setCandidates] = useState([])
    const [eliminated, setEliminated] = useState([])
    const [active, setActive] = useState(true)
    const [loaded, setLoaded] = useState(false)

    useEffect(()=> {
        //TODO: Check if a winner is already announced or if game is even active

        
        getCandidates()
        getEliminated()

        checkActive().then(async is_active => {
            await is_active ? getCurrentRoundDetails() : setActive(false)
            setLoaded(true)
        })
        

        const socket = io(`${SOCKET_BASE}/${uid}`);
        socket.on("round_end", data => {
            getCandidates()
            getEliminated()
            if (data.winner.overall) {
                alert(`${data.winner.name} has won!`)
            } else{
                getCurrentRoundDetails()
            }
            
        })
        socket.on("vote_cast", data => {
            setCurrentRound(formatScores(data.results))
        })
    }, [])

    const getCurrentRoundDetails = async () => {
        fetch(`http://localhost:5000/api/current_round?uid=${uid}`)
            .then(response => response.json())
            .then(data => {
                setCurrentRoundId(data.ref)
                setCurrentRound(formatScores(data.scores))
            })
            .catch(err => console.log(err))
    }
    const getCandidates = async () => {
        fetch(`http://localhost:5000/api/candidates?uid=${uid}`, {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                setCandidates(data.data)
            })
            .catch(err => {
                console.log('error handling to be introduced')
            })
    }

    const getEliminated = async () => {
        fetch(`http://localhost:5000/api/results?uid=${uid}`, {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                setEliminated(Object.keys(data.data).filter(i => i!=="CURRENT_ROUND"))
            })
            .catch(err => {
                console.log('error handling to be introduced')
            })
    }

    const castVote = async name => {
        fetch("http://localhost:5000/api/vote", 
            {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "POST",
                body: JSON.stringify({
                    "uid": uid,
                    "round": currentRoundId,
                    "vote": name
                })
            })
    }

    const endRound = () => {
        fetch(`http://localhost:5000/api/end_round?uid=${uid}&ref=${currentRoundId}`)
    }

    const checkActive = () => (
        fetch(`http://localhost:5000/api/is_active?uid=${uid}`)
            .then(response => response.json())
            .then(data => data.active)
    )

    const formatScores = raw => {
        const keys = Object.keys(raw).sort((a,b)=>{
            return a[0].toLowerCase() > b[0].toLowerCase()
        })
        let scores = [{},{}]
        for (let i=0; i < 2; i++){
            scores[i]["name"] = keys[i]
            scores[i]["votes"] = raw[keys[i]]
        }
        return scores
    }

    return(
        <div>
            <h1>Hello</h1>
            <p>{uid}</p>
            {loaded && <>
            {active ? <p>Currently active</p> : <p>Voting has finished, winner is {candidates[0]}</p>}
            {currentRound.map(score => (
                <p onClick={() => castVote(score.name)}>{score.name} - {score.votes}</p>
            ))}

            <div 
                onClick={endRound}
                style={{cursor: 'pointer'}}
            >End Round</div>

            <div style={{display: 'flex'}}>
                <div style={{color: 'green'}}>
                    {candidates.map(candidate => (
                        <p>{candidate}</p>
                    ))}
                </div>
                <div style={{color: 'red'}}>
                    {eliminated.map(candidate => (
                        <p>{candidate}</p>
                    ))}
                </div>
            </div>
            </>}
        </div>
    )
}

export default Voting