<template>
    <div id = "main">
        <div id = "formbody">
            <h1 Style = "text-align: center;">{{ isEditing ? "Edit Profile form" : "StudentRegister form" }}</h1>
            <form @submit.prevent="handleStudentregister">
                <div v-if = "errorMessage">
                    <h1> Something went wrong: {{errorMessage}}</h1>
                </div>
                <div v-else>
                    <div v-if="isEditing">
                        <div>
                            <label class = "mx-3 " for="email">Email:</label>
                            <input type='email' id="email" v-model="form.email" required>
                        </div>
                    </div>
                    <div >
                        <label  class = "mx-3 my-3 " for="name">Name:</label>
                        <input type = 'text' id ="name" v-model = "form.name"  required>
                    </div>
                    <div>
                        <label class = "mx-3 my-3" for="branch">Branch:</label>
                        <input type = 'text' id ="branch" v-model = "form.branch" required>
                    </div>
                    <div>
                        <label class = "mx-3 my-3" for="year">Year:</label>
                        <input type = 'text' id ="Year" v-model = "form.year" required>
                    </div>
                    <div>
                        <label class = "mx-3 my-3" for="cgpa">Cgpa:</label>
                        <input type = "number" id ="cgpa" v-model = "form.cgpa" required>
                    </div>
                    <div>
                        <label class = "mx-3 my-3" for="phone">Phone:</label>
                        <input type = 'number' id ="phone" v-model = "form.phone" required>
                    </div>
                    <div>
                        <label class = "mx-3 my-3" for="skills">Skills:</label>
                        <input type = 'text' id ="skills" v-model = "form.skills" required>
                    </div>
                    <h9 class = "mx-3 my-3">Please add at least one skill after one skill add comma</h9>
                    <div style = "text-align: center;">
                        <button class = "btn btn-primary me-3 mb-3" type="submit">{{ isEditing ? "SaveChanges" : "Register"}}</button><br>
                        <button v-if="isEditing" class = "btn btn-primary me-3 mb-3" type="submit" @click="$router.push('/student/dashboard')" >Back</button>
                        <button  v-else class = "btn btn-primary me-3 mb-3" type="submit" @click = "$router.push('/user')">Back</button>

                    </div>
                    

                </div>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
    export default{
        name:'StudentRegister',
        emits:['profile-completed'],
        data(){
            return{
                isEditing: false,
                form:{
                    name:'',
                    branch:'',
                    year:'',
                    cgpa:0,
                    phone:0,
                    skills:'',
                    email:'',
                },
                errorMessage: ''
            }
        },
        async mounted() {
            try{
                const token = localStorage.getItem('token');
                if(!token){
                    alert("Token not found. Please log in.");
                    return; // Stop execution if there's no token
                }
                const response = await axios.get('http://localhost:5000/api/student_profile', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.data && response.data.exists === true) {
                    this.form = response.data;
                    this.isEditing = true;
                }else if(response.data ){
                    this.form.email = response.data.email;
                }

            } catch (error){
                console.log("No preious profile found, please register");
            }
        },
        // Inside your Vue Component <script> tag:
        methods: {
            async handleStudentregister(){
                try {
                    const token = localStorage.getItem('token');
                    if(!token){
                        alert("Token not found. Please log in.");
                        return; // Stop execution if there's no token
                    }
                    
                    
                    const response = await axios.post('http://localhost:5000/api/register/student', this.form, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    this.$emit('profile-completed', response.data);
                    alert(this.isEditing ? "Profile updated successfully!" : "Registration successful!");
                    this.$router.push('/student/dashboard');
                } catch(error) {
                    console.error('Registration failed:', error.response ? error.response.data : error.message);
                    if (error.response && error.response.data && error.response.data.message) {
                    this.errorMessage = error.response.data.message;
                    } else {
                    this.errorMessage = "Something went wrong. Please try again.";
                    }
                    alert("Registration failed. Please check the console for details.");
                }
            }
        }
    }
</script>
<style scoped>
    *{
        margin:0px;
    }

    #main{
    min-height: 100vh;
    background-color: #d9f3ff;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 40px;
    }

    #formbody{
        width: 500px;
        border: 9px solid gray;
        border-radius: 5px;
        padding: 10px;
        margin: 0;
        height: auto;
    }
    #canvas{
        margin: auto;
        height: 800px;
        width:60%;
        border:2px solid white;
    }
    /* #formbody{
        border:9px solid gray;
        width :500px;
        height:500px;
        margin: auto;
        border-radius: 5px;
        margin-top: 40px;
        align-items: center;
        padding:10px;
    } */
    #Table{
        padding: 8px;
        margin-top: 1px;
    }
</style>