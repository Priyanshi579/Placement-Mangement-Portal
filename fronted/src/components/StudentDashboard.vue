<template>
    <div id="main" class="d-flex justify-content-center ">
        <div id="canvas">
            <div id= nav>
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid d-flex justify-content-between align-items-center">
                        <a class="navbar-brand mb-0 h1" style="color:brown">Welcome {{ studentName }}</a>
                        <div class="d-flex gap-2">
                            <button type="button" class="btn btn-info" @click = "$router.push('/update_student')">Edit Profile</button>
                            <button type="button" class="btn btn-success" @click = "$router.push(`/applied_history/${student_id}`)">history</button>
                            <button type="button" class="btn btn-danger" @click = "logout()">logout</button>
                            <button type="button" class="btn btn-warning" @click = "this.$router.push('/')">Back</button>
                            <button type="button" class="btn btn-dark me-3" @click = "trigger()">Get application history on mail</button>
                        </div>
                    </div>
                </nav>
                <br>
                <div class="px-2">
                    <nav class="d-flex flex-column">
                        <button class="btn btn-primary" @click = "active = 'company'"> Companys</button>
                        <br><br><StudentCompany v-if = "active === 'company'"></StudentCompany>
                        <button class="btn btn-primary" @click = "active = 'applied'">Applied drives</button>
                        <AppliedDrive v-if = "active === 'applied'"></AppliedDrive><br><br>
                        <button class="btn btn-primary" @click = "active = 'summary'">click to see summary of apply drives</button>
                        <UserSummary v-if = "active === 'summary'"></UserSummary>
                    </nav>
                </div>
                <!-- <div>
                    <main>
                        <OngoingDrive v-if = "active === 'ongoing'"></OngoingDrive>
                        <ClosedDrive v-if = "active === 'closed'"></ClosedDrive>
                    </main>
                </div> -->
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import StudentCompany from '../components/StudentCompany.vue'
import AppliedDrive from '../components/AppliedDrive.vue'
import UserSummary from '../components/UserSummary.vue'
export default{
    name: 'StudentDashboard',
    components:{
        StudentCompany,
        AppliedDrive,
        UserSummary

        
    },
    props: ['logged_student'],
    data(){
        return{
            active:'hii',
            studentName: '',
            student_id: '',
            msg : 'null'
        }
    },
    async mounted() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                this.$router.push('/'); 
                return;
            }
            const response = await axios.get('http://localhost:5000/api/student_profile', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.data && response.data.exists === true) {
                this.studentName = response.data.name;
                this.student_id = response.data.id;
            }
        } catch (error) {
            console.error("Failed to load student name on dashboard mounting:", error);
        }
    },
    methods:{
        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');

        },
        async trigger(){
            try{
                const token = localStorage.getItem('token');
                const response = await axios.get('http://localhost:5000//api/export/application_history',{
                    headers:{
                        'Content-Type': 'Application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                this.msg = response.data;
                alert("check your mail please");

            }catch(error){
                console.log(error);
                alert(error.response.data.message);
            }
        }
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
    background-color:#d9f3ff;
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
