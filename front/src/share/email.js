import Swal from "sweetalert2";

export const show_mail_confirm_swal = (handle) => {
  Swal.fire({
    icon: "warning",
    title: "信箱驗證",
    text: "驗證信應已寄至您的信箱，請確認並驗證郵件！",
    showDenyButton: true,
    confirmButtonText: "OK",
    denyButtonText: "沒有收到信，重寄一封",
  }).then((result) => {
    if (result.isDenied) {
      run_resend_email(handle);
    }
  });
};

export const run_resend_email = (account) => {
  $.ajax({
    url: "/api/auth/resend_email?account=" + account,
    type: "POST",
    success: function (data, status, xhr) {
      success_swal("信件已寄送");
    },
    error: function (xhr, exception) {
      if (xhr.status == 422) {
        error_swal("寄送失敗", "登入使用的 Handle 或信箱尚未註冊");
      } else if (xhr.status == 403) {
        error_swal("寄送失敗", "信箱驗證設置尚未開啟");
      }
    },
  });
};
