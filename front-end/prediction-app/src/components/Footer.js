import React from "react" ;
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';

function Footer(){
    return(
        <Typography variant ="body2" align ="center">
            {'Copyright © '}
            <Link color="inherit" href="#">
               Diabetes Predictor
            </Link>{' '}
                {new Date().getFullYear()}
                {'.'}
        </Typography>   

    );
}

export default Footer