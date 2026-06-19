<template>
    <div>
        <h1 style = "text-align: center;">List of Applied Student</h1>
        <div class = "table" style = "text-align: center;">
            <table border = "10px" bordlinecolor="white">
                <thead>
                    <th>Name</th>
                    <th>Company Name</th>
                    <th>Drive Name</th>
                    <th>Application Date</th>
                    <th>Action</th>
                </thead>
                <tbody>
                    <tr v-for = "data in applied_student" :key = "data.id">
                        <td>{{data.student_name}} </td>
                        <td>{{data.company_name}} </td>
                        <td>{{data.drive_name}} </td>
                        <td>{{data.application_date}} </td>
                        <td><button class="btn btn-success"  @click = "viewdetails(data.id)">View Details</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
</template>
<script>
import axios from 'axios'
export default{
    name:'StudentApplication',
    data(){
        return{
            applied_student:[]
        }
    },
    methods:{
        async fetchapplystudentdetails(){
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/application',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            console.log(res.data)
            this.applied_student = res.data
            
        },
        viewdetails(id){
            this.$router.push({name:'StudentDetails',params:{id:id}});
        }
        
        

    },
    mounted(){
        this.fetchapplystudentdetails()
    }
}
</script>

<style scoped>
    .table{
        border:none;
        margin-top:10px;
        width:715px;
        /* ADD THESE THREE LINES TO CENTER THE CANVAS: */
        display: flex;
        justify-content: center; /* Centers horizontally */
        align-items: flex-start; /* Keeps the canvas layout sticking towards the top */
        /* min-height: 100vh; */
    }
</style>
