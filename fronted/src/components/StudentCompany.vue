<template>
    <div>
        <h1 style = "text-align: center;">List of Company</h1>
        <div class = "table" style = "text-align: center;">
            <table border = "10px" bordlinecolor="white" style="margin: auto; border-collapse: collapse;">
                <thead>
                    <tr>
                        <td style="padding: 10px 40px;">Name</td>
                        <td style="padding: 10px 40px;">Action</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for = "company in company_details" :key = "company.id">
                        <td style="padding: 15px 40px;">{{company.name}} </td>
                        <td style="padding: 15px 40px;"><button class="btn btn-primary"  @click="viewdetails(company.id)">view details</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name:'StudentCompany',
    data(){
        return{
            company_details:[]
        }
    },
    methods:{
        async fetchcompanydetails(){
            const token = localStorage.getItem('token');
            const res = await axios.get('http://localhost:5000/api/get/student/company',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            this.company_details = res.data
            
        },
        
        viewdetails(id){
            this.$router.push({name: 'CompanyDrives', params: {id: id}});
            }
    },
    mounted(){
        this.fetchcompanydetails()
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
