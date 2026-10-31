
<template>
  <div class="approval-container">
    <div class="approval-card">
      <div class="icon">⏳</div>

      <h1>Account Pending Approval</h1>

      <p>
        Your company registration has been completed successfully.
      </p>

      <p>
        Your account is currently awaiting administrator approval.
        You will be able to access your company dashboard once
        your account has been approved.
      </p>

      <div class="status">
        Status: Pending
      </div>

      <p class="footer">
        Thank you for your patience!
      </p>
    </div>
  </div>
</template>

<style scoped>
.approval-container {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: #f5f7fb;
}

.approval-card {
  max-width: 550px;
  width: 100%;
  padding: 40px 30px;
  text-align: center;
  background: white;
  border-radius: 14px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
}

.icon {
  font-size: 55px;
  margin-bottom: 15px;
}

h1 {
  color: #243b53;
  font-size: 26px;
  margin-bottom: 20px;
}

p {
  color: #52606d;
  line-height: 1.7;
}

.status {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 22px;
  background: #fff3cd;
  color: #856404;
  border-radius: 20px;
  font-weight: bold;
}

.footer {
  margin-top: 25px;
}
</style>

