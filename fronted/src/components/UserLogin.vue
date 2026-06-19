<template>
    <div id = "main">
        <div id = "formbody">
            <form @submit.prevent="handle_Login">
                
                <div>
                    <h1 Style = "text-align: center;">Login form</h1>
                    <div class="mb-3">
                        <label class= "me-3"for="username">Username:</label>
                        <input type = 'text' id ="username" v-model = "form.username"  required>
                    </div>
                    <div class="mb-3">
                        <label  class= "me-5" for="email">Email:</label>
                        <input type = 'text' id ="email" v-model = "form.email" required>
                    </div>
                    <div class="mb-3">
                        <label class= "me-3" for="password">Password:</label>
                        <input type = 'text' id ="password" v-model = "form.password" required>
                    </div> 
                    
                    <div class = "text-center">
                        <button  class = "btn btn-primary mb-3" type="submit">Login</button><br>
                        <button  class = "btn btn-info" type="submit" @click = "$router.push('/')">back</button><br>
                        <a href = "#" @click.prevent="$emit('register-here')">Don't have account? Register</a>
                        
                    </div>
                    
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
        name:'UserLogin',
        emits:['logged','register-here'],
        data(){
            return{
                form:{
                    username:'',
                    email:'',
                    password:''
                },
                errorMessage: ''
            }
        },
        methods: {
            async handle_Login(){
                try{
                    const response = await axios.post('http://localhost:5000/api/login',this.form)
                    console.log('Login response',response.data)
                    // this.$emits('login')        
                    localStorage.setItem('token',response.data.data.access_token)
                    this.$emit('logged',{
                        role:response.data.data.role,
                        profileCompleted:response.data.profile_completed,
                        username: response.data.data.username,
                        approval_status:response.data.approval_status 
                    }); 
                }
                catch(error){
                    console.log('Login failed', error)

                    if (error.response && error.response.data && error.response.data.message ) {
                    this.errorMessage = error.response.data.message;
                    alert(error.response.data.message);
                    } else {
                    this.errorMessage = "Something went wrong. Please try again.";
                    }
                    this.form.username = '';
                    this.form.password = '';
                    this.form.email = '';
                }
            }
                
        }   
    }

</script>
<style scoped>
    #main{
        border:2px solid #d9f3ff;
        background-color: #d9f3ff;
        display: flex;
        justify-content: center; /* Centers horizontally */
        align-items: center;     /* Centers vertically */
        width: 100vw;            /* Take exactly 100% of browser window width */
        height: 100vh;
    }

    #canvas{
        margin: auto;
        height: 800px;
        width:60%;
        border:2px solid white;
    }
    #formbody{
        border:9px solid gray;
        width :420px;
        height:350px;
        margin: 6%;
        border-radius: 5px;
        margin-top: 177px;
        padding:20px;
    }


</style>
