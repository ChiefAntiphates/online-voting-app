import React, { useEffect, useState } from "react";
import {useNavigate} from "react-router-dom"

const Create = props => {
    const navigate = useNavigate()
    
    const [candidates, setCandidates] = useState([])
    const [newCandidate, setNewCandidate] = useState()
    const newTournament = () => {
        fetch(`http://localhost:5000/api/new`, {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    entries: candidates
                })
            })
            .then(response => response.json())
            .then(data => {
                navigate(`/vote/${data.uid}`)
            })
    }

    const addCandidate = () => {
        setCandidates(prev => [...prev, newCandidate])
        setNewCandidate('')
    }

    const removeCandidate = i => {
        console.log('hi')
        setCandidates(prev => prev.filter((_, j)=>j!==i))
    }

    return(
        <div>
            <div>Entries</div>
            {candidates.map((candidate, i) => (
                <p onClick={()=>removeCandidate(i)}>{candidate}</p>
            ))}
            <input value={newCandidate} onChange={e => setNewCandidate(e.target.value)} />
            <div onClick={addCandidate}>Add</div>
            <hr/>
            <div onClick={newTournament}>Submit</div>
        </div>
    )
}

export default Create