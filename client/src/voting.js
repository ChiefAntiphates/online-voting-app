import React from "react";
import { useLocation, useParams } from 'react-router-dom';

const Voting = props => {
    const params = useParams()
    return(
        <div>
            <h1>Hello</h1>
            <p>{params.id}</p>
        </div>
    )
}

export default Voting