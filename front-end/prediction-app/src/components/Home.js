import * as React from 'react'
import axios from 'axios';
import * as settings from '../settings';
import CssBaseline from '@material-ui/core/CssBaseline';
import { makeStyles } from '@material-ui/core/styles';
import { Container, Grid, Paper, Typography, Slider, Button} from '@material-ui/core';
import {TextField, Select,MenuItem,Box,InputLabel,FormControl} from '@material-ui/core';
 
 
// ########################################################
// Material UI inline styles
// ########################################################
const useStyles = makeStyles((theme) => ({
    container: {
        maxWidth: "75%",
        marginTop: "15vh",
        marginBottom: "10vh",
        borderRadius: '6px',
        backgroundColor: theme.palette.action.disabledBackground,
    },
    title: {
        marginTop: theme.spacing(2),
        marginBottom: theme.spacing(2),
        padding: theme.spacing(2), paddingLeft: theme.spacing(4),
        color: theme.palette.primary.main,
    },
    sliders: {
        paddingTop: theme.spacing(2),
        paddingBottom: theme.spacing(2),
        paddingLeft: theme.spacing(4),
        paddingRight: theme.spacing(4),
        marginBottom: theme.spacing(2),
    },
    slidertop: {
        marginTop: theme.spacing(4),
    }
}));

// ########################################################
// Our Custom slider. You may use the default slider instead of this
// ########################################################
// const MySlider = withStyles({
//     root: {
//         color: '#751E66',
//     },
//     valueLabel: {
//         left: 'calc(-50% -2)',
//         top: -22,
//         '& *': {
//             background: 'transparent',
//             color: '#000',
//         },
//     },
//     mark: {
//         height: 8,
//         width: 1,
//         marginTop: -3,
//     },
//     markActive: {
//         opacity: 1,
//         backgroundColor: 'currentColor',
//     },
// })(Slider);

// ########################################################
// The main Home component returned by this Module
// ########################################################
function Home(props) {
    // Material UI Classes 
    const classes = useStyles();

    // React hook state variable - Dimensions
    const [dimensions, setDimensions] = React.useState({
        gender:'Male',
        age:35,
        hypertension:0,
        heart_disease:0,
        smoking_history:'No Info',
        bmi: 20.5,
        HbA1c_level: 5.0,
        blood_glucose_level: 80
    });

    // Function to update the Dimensions state upon slider value change
    const handleSliderChange = name => (event, newValue) => {
        setDimensions(
            {
                ...dimensions,
                ...{ [name]: newValue }
            }
        );
    };
    
    const handleChange = (name)=>(event) => {
        setDimensions(
            {
                ...dimensions,
                ...{ [name]: event.target.value }
            }
        );
    };

     // React hook state variable - Prediction
     const [prediction, setPrediction] = React.useState('click predict button to get result');


    // Function to make the predict API call and update the state variable - Prediction 
    const handlePredict = event => {
        // Submit measured dimensions as form data
        console.log(dimensions)
        const jsonArray = [];
        jsonArray.push(dimensions)
        const jsonString = JSON.stringify(jsonArray);
        console.log(jsonString)
        const jsonObject = JSON.parse(jsonString);
        console.log(jsonObject)
        //Axios variables required to call the predict API
        let headers = { 'Authorization': `Token ${props.token}` };
        let url = settings.API_SERVER + '/diabetes_predict';
        let method = 'post';
        let config = { headers, method, url, data: jsonObject };
        //Axios predict API call
        axios(config)
        .then(res => {
            const result = res.data;
            if(result=='0') {
                setPrediction(<font color='green'>congratulations! No diabetes risk.</font>)
            }
            else if(result=='1') {
                setPrediction(<font color='red'>It is crucial to be mindful of the risk of diabetes.</font>)
            }else {
                setPrediction("Prediction error, please adjust dimentions and try it again!")
            }
        })
        .catch(error => {alert(error)});
        console.log(prediction)
    }

    return (
        <React.Fragment>
            <CssBaseline />
            <Container fixed className={classes.container}>
                <Grid container alignItems="center" spacing={3}>
                    <Grid item xs={6}>
                        <Paper className={classes.title} elevation={0}>
                            <Typography variant="h5">
                                Patient Dimensions
                            </Typography>
                        </Paper>
                        <Paper className={classes.sliders}>
                        <Box>
                            <FormControl variant="standard">
                                <TextField id="age-component" label="Age" style={{ width: '380px' }} 
                                value={dimensions.age} onChange={handleChange('age')}/>
                            </FormControl>
                            <FormControl variant="standard">
                            <InputLabel id="gender-select-label">Gender</InputLabel>
                            <Select style={{ width: '190px' }}
                            labelId="gender-select-label"
                            id="gender-select"
                            label="Gender" value={dimensions.gender} onChange={handleChange('gender')}>
                            <MenuItem value={'Male'}>Male</MenuItem>
                            <MenuItem value={'Female'}>Female</MenuItem>
                            <MenuItem value={'Other'}>Other</MenuItem>
                            </Select> 
                        </FormControl>
                        <FormControl variant="standard">
                            <InputLabel id="heart-disease-select-label">Heart_Disease</InputLabel>
                            <Select style={{ width: '190px' }}
                            labelId="heart-disease-select-label"
                            id="heart-disease-select"
                            label="Heart_Disease" value={dimensions.heart_disease} onChange={handleChange('heart_disease')}>
                            <MenuItem value={0}>No</MenuItem>
                            <MenuItem value={1}>Yes</MenuItem>
                            </Select> 
                        </FormControl>
                        <FormControl variant="standard">
                        <InputLabel id="hypertension-select-label">Hypertension</InputLabel>
                            <Select style={{ width: '190px' }}
                            labelId="hypertension-select-label"
                            id="hypertension-select"
                            label="Hypertension" value={dimensions.hypertension} onChange={handleChange('hypertension')}>
                            <MenuItem value={0}>No</MenuItem>
                            <MenuItem value={1}>Yes</MenuItem>
                            </Select>
                        </FormControl>
                        <FormControl variant="standard">
                        <InputLabel id="smoke-history-select-label">Smoke_History</InputLabel>
                            <Select style={{ width: '190px' }}
                            labelId="smoke-history-select-label"
                            id="smoke-history-select"
                            label="Smoke_History" value={dimensions.smoking_history} onChange={handleChange('smoking_history')}>
                            <MenuItem value={'No Info'}>No Info</MenuItem>
                            <MenuItem value={'current'}>Current</MenuItem>
                            <MenuItem value={'ever'}>Ever</MenuItem>
                            <MenuItem value={'former'}>Former</MenuItem>
                            <MenuItem value={'never'}>Never</MenuItem>
                            <MenuItem value={'not current'}>Not current</MenuItem>
                            </Select>
                        </FormControl>
                        </Box>
                        </Paper>
                        <Paper className={classes.sliders}>
                            <Typography id="bmi_text" variant="body1" gutterBottom>
                                BMI 
                            </Typography>
                            <Slider
                                defaultValue={20.5}
                                aria-labelledby="bmi"
                                step={0.1}
                                min={0}
                                max={100}
                                valueLabelDisplay="on"
                                className={classes.slidertop}
                                onChange={handleSliderChange("bmi")}
                            />
                            <Typography id="hba1c_text" variant="body1" gutterBottom>
                                HbA1c_level (%)
                            </Typography>
                            <Slider
                                defaultValue={5.0}
                                aria-labelledby="HbA1c_level"
                                step={0.1}
                                min={0.1}
                                max={20}
                                valueLabelDisplay="on"
                                className={classes.slidertop}
                                onChange={handleSliderChange("HbA1c_level")}
                            />
                            <Typography id="blood_text" variant="body1" gutterBottom>
                                Blood_glucose_level (mg/dL)
                            </Typography>
                            <Slider
                                defaultValue={80}
                                aria-labelledby="blood_glucose_level"
                                step={1}
                                min={1}
                                max={200}
                                valueLabelDisplay="on"
                                className={classes.slidertop}
                                onChange={handleSliderChange("blood_glucose_level")}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <Button variant="contained" color="primary" onClick={handlePredict}>
                            Predict
                        </Button>
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.title} elevation={0}>
                            <Typography variant="caption" display="inline">
                                Predicted Results: <span>&nbsp;</span>
                            </Typography>
                            <Typography variant="body1" display="inline">
                                {prediction}
                            </Typography>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        </React.Fragment>
    )
}
    
export default Home