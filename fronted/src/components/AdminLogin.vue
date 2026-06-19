<template>
    <div id = "main">
        <div id = "formbody">
            <form @submit.prevent="handle_Login">
                <div v-if = "errorMessage">
                    <h1> Something went wrong: {{errorMessage}}</h1>
                </div>
                <div v-else>
                    <h1 Style = "text-align: center;">Admin Login form</h1>
                    <div class="mb-3">
                        <label for="username">Username:</label>
                        <input type = 'text' id ="username" v-model = "form.username"  required>
                    </div>
                    <div class="mb-3">
                        <label for="email">Email:</label>
                        <input type = 'text' id ="email" v-model = "form.email" required>
                    </div>
                    <div class="mb-3">
                        <label for="password">Password:</label>
                        <input type = 'text' id ="password" v-model = "form.password" required>
                    </div> 
                    
                    <div class = "text-center">
                        <button  class = "btn btn-primary" type="submit">Login</button><br>
                        <button  class = "btn btn-info" type="submit" @click = "$router.push('/')">Back to Home</button>
                        
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name:'AdminLogin',
    emits:['logged'],
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
                const response = await axios.post('http://localhost:5000/api/adminlogin',this.form)
                console.log('Login response',response.data)
                // this.$emits('login')        
                localStorage.setItem('admin_token',response.data.data.access_token)
                this.$emit('logged'); 
            }
            catch(error){
                console.log('Login failed', error)

                if (error.response && error.response.data && error.response.data.message) {
                this.errorMessage = error.response.data.message;
                } else {
                this.errorMessage = "Something went wrong. Please try again.";
                }
            }
        }
            
    }   
}
</script>
<style scoped>
    #main{
        border:2px solid #d9f3ff;
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
        border:2px solid #d9f3ff;
    }
    #formbody{
        border:9px solid #d9f3ff;
        width :420px;
        height:312px;
        margin: 6%;
        border-radius: 5px;
        margin-top: 177px;
        padding:20px;
    }


</style>