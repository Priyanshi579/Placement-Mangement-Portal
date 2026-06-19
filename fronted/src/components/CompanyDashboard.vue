<template>
    <div id="main" class="d-flex justify-content-center">
        <div id="canvas">
            <div id= nav>
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid">
                        <a class="navbar-brand" style="color:brown">Welcome {{ company_name }}</a>
                        <header class="d-flex justify-content-end mb-4">
                            <button type="button" class="btn btn-info me-3" @click = "$router.push('/create_drive')">Create Drive</button>
                            <button type="button" class="btn btn-danger me-3" @click = "logout()">logout</button>
                            <button type="button" class="btn btn-warning" @click = "this.$router.push('/')">Back</button>
                            
                        </header>
                    </div>
                </nav>
                <br>
                
                <div class="px-2">
                    <nav class="d-flex flex-column">
                        <button class="btn btn-primary" @click = "active = 'ongoing'">Ongoing drive</button>
                        <br><br><OngoingDrive v-if = "active === 'ongoing'"></OngoingDrive>
                        <button class="btn btn-primary" @click = "active = 'closed'">Closed drive</button>
                        <ClosedDrive v-if = "active === 'closed'"></ClosedDrive>
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
import OngoingDrive from '../components/OngoingDrive.vue'
import ClosedDrive from '../components/ClosedDrive.vue'
export default{
    name: 'CompanyDashboard',
    components:{
        OngoingDrive,
        ClosedDrive

        
    },
    props: ['logged_company'],
    data(){
        return{
            active:'hii',
            company_name:"",
            company_id:""
        }
    },
    async mounted(){
        try{
            const token = localStorage.getItem('token');
            if (!token){
                this.$router.push('/');
                return;
            }
            const response =  await axios.get('http://localhost:5000/api/company_profile', {
                headers:{
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.data && response.data.exists === true){
                this.company_name = response.data.name;
                this.company_id = response.data.id;
            }
        }
        catch(error){
            console.error("Failed to load company name on dashboard mounting:", error);
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
    /* margin-top:10px; */
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
