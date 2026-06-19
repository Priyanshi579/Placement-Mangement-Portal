<template>
    <div id="main" class="d-flex justify-content-center">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid justify-content-between align-items-center">
                        <a class="navbar-brand mb-0 h1" style="color:brown">Welcome {{ student_name }}</a>
                        <div>
                            <button type="button" class="btn btn-danger me-3" @click = "logout()">logout</button>
                            <button type="button" class="btn btn-warning" @click = "this.$router.push('/student/dashboard')">Back</button>
                        </div>

                    </div>
                    <div id="content" class="px-2">
                    <header class="d-flex justify-content-end mb-4">
                        
                    </header>
                    </div>
                </nav>
                <br>
                <div><h1 style = "text-align: center;">History of applications</h1>
                    
                </div>
                <br>
                <div>
                    <h1 style = "text-align: center;">List of Apllied drives</h1>
                    <div class = "table" style = "text-align: center;">
                        <table border = "10px" bordlinecolor="white" style="margin: auto; border-collapse: collapse;">
                            <thead>
                                <tr>
                                    <td style="padding: 10px 40px;">Name</td>
                                    <td style="padding: 10px 40px;">job title</td>
                                    <td style="padding: 10px 40px;">Company Name</td>
                                    <td style="padding: 10px 40px;">Result</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for = "application in applied_drives" :key = "application.id">
                                    <td style="padding: 15px 40px;">{{application.name}} </td>
                                    <td style="padding: 15px 40px;">{{application.jobtitle}} </td>
                                    <td style="padding: 15px 40px;">{{application.company}} </td>
                                    <td style="padding: 15px 40px;">{{application.status}} </td>
                                    <!-- <td style="padding: 15px 40px;"><button class="btn btn-primary"  @click="viewdetails(drive.id)">view details</button></td> -->
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <!-- <div id="content" class="px-2">
                    <header class="d-flex justify-content-end mb-4">
                        <button type="button" class="btn btn-danger" @click = "logout()">logout</button>
                    </header>
                </div> -->
                
            </div>
        </div>
    </div>
        
</template>

<script>
import axios from 'axios'
export default{
    name:'HistoryView',
    components:{
        
    },
    data(){
        return{
            applied_drives : [],
            student_name : ''
        }
    },
    async mounted() {
            try{
                const token = localStorage.getItem('token');
                if(!token){
                    alert("Token not found. Please log in.");
                    this.$router.push('/');
                    return; 
                }
                const student_id  = this.$route.params.student_id;
                console.log("student_id =", student_id);
                const response = await axios.get(`http://localhost:5000/api/applied_history/${student_id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                this.applied_drives = response.data.data;
                this.student_name = response.data.details.student_name;
            } catch (error){
                console.log("Some error occured : ", error);
            }
        },
    methods:{
        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');

        },
    }
}
</script>

<style scoped>
#main{
    width:100%;
    min-height:100vh;
    margin-top:10px;
    background-color:#d9f3ff;

    display:flex;
    justify-content:center;
    align-items:flex-start;
}

#canvas{
    /* margin: auto; */
    height: 800px;
    width:60%;
    border:2px solid white;
}
#formbody{
    border:9px solid gray;
    width :300px;
    height:400px;
    margin: auto;
    border-radius: 5px;
    margin-top: 200px;
    padding:10px;
}
#Table{
    padding: 8px;
    margin-top: 1px;
}

</style>
