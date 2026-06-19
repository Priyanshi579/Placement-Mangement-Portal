<template>
    <div id="main" class="d-flex justify-content-center ">
        <div id="canvas">
            <div id= "nav">
                <nav class="navbar bg-primary" data-bs-theme="dark">
                    <div class="container-fluid justify-content-between align-items-center">
                        <a class="navbar-brand mb-0 h1" style="color:brown">Welcome {{ company_name }}</a>
                        <div>
                            <button type="button" class="btn btn-danger me-3" @click = "logout()">logout</button>
                            <button type="button" class="btn btn-info" @click = "this.$router.push('/student/dashboard')">Back</button>
                        </div>
                    </div>
                    <div id="content" class="px-2">
                    <header class="d-flex justify-content-end mb-4">
                        
                    </header>
                    </div>
                </nav>
                <br>
                <div><h1 style = "text-align: center;">Overview</h1>
                    <p style = "text-align: center;">we give equally opporuntity to all candidate . Our process of selction is fair and honest</p>
                </div>
                <br>
                <div>
                    <h1 style = "text-align: center;">List of Drives</h1>
                    <div class = "table" style = "text-align: center;">
                        <table border = "10px" bordlinecolor="white" style="margin: auto; border-collapse: collapse;">
                            <thead>
                                <tr>
                                    <td style="padding: 10px 40px;">Name</td>
                                    <td style="padding: 10px 40px;">job title</td>
                                    <td style="padding: 10px 40px;">Salry</td>
                                    <td style="padding: 10px 40px;">Action</td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for = "drive in drives" :key = "drive.id">
                                    <td style="padding: 15px 40px;">{{drive.name}} </td>
                                    <td style="padding: 15px 40px;">{{drive.jobtitle}} </td>
                                    <td style="padding: 15px 40px;">{{drive.salary}} </td>
                                    <td style="padding: 15px 40px;"><button class="btn btn-primary"  @click="viewdetails(drive.id)">view details</button></td>
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
    name:'CompanyDrives',
    components:{
        
    },
    data(){
        return{
            drives : [],
            company_name : ''
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
                const company_id  = this.$route.params.id;
                const response = await axios.get(`http://localhost:5000/api/company_drives/${company_id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                this.drives = response.data.data;
                this.company_name = response.data.details.name;
            } catch (error){
                console.log("Some error occured : ", error);
            }
        },
    methods:{
        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');

        },
        viewdetails(id){
            this.$router.push({name:'DriveDetails', params:{id:id}});
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
