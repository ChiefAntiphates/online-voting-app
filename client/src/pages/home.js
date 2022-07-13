import React, { useEffect, useState } from "react";
import {useNavigate} from "react-router-dom"

const Home = props => {
    const navigate = useNavigate();

    
    return(
        <div>
            <div onClick={()=>navigate('/create')}>New Tournament</div>
        </div>
    )
}

export default Home;