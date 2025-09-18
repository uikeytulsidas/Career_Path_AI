from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .utils import extract_skill_and_recommendations  # ensure this returns dict/json

# class GeminiAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         resume_text = request.data.get("resume_text")
#         if not resume_text:
#             return Response(
#                 {"error": "Resume text is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             user = request.user if request.user.is_authenticated else None
#             tokens_used = len(resume_text.split())  # rough token count

#             if user:
#                 # logged-in user → 300 tokens
#                 session = request.session
#                 used_tokens = session.get(f"user_{user.id}_tokens", 0)

#                 if used_tokens + tokens_used > 300:
#                     return Response(
#                         {"error": "Token limit (300) reached. Please upgrade or wait for reset."},
#                         status=403,
#                     )

#                 result = extract_skill_and_recommendations(resume_text)

#                 session[f"user_{user.id}_tokens"] = used_tokens + tokens_used
#                 session.save()

#                 return Response({
#                     "response": result,
#                     "remaining_tokens": 300 - session[f"user_{user.id}_tokens"]
#                 }, status=status.HTTP_200_OK)

#             else:
#                 # guest → 50 tokens
#                 session = request.session
#                 used_tokens = session.get("guest_tokens", 0)

#                 if used_tokens + tokens_used > 50:
#                     return Response(
#                         {"error": "Free trial limit (50 tokens) reached. Please login to continue."},
#                         status=403,
#                     )

#                 result = extract_skill_and_recommendations(resume_text)

#                 session["guest_tokens"] = used_tokens + tokens_used
#                 session.save()

#                 return Response({
#                     "response": result,
#                     "remaining_tokens": 50 - session["guest_tokens"]
#                 }, status=status.HTTP_200_OK)

#         except Exception as e:
#             print(f"Error during career analysis: {e}")
#             return Response(
#                 {"error": f"Failed to analyze resume: {e}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


class GeminiAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        resume_text = request.data.get("resume_text")
        if not resume_text:
            return Response({"error": "Resume text is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user if request.user.is_authenticated else None

        try:
            result = extract_skill_and_recommendations(resume_text)  # dict with skills & recommendations

            # Token logic
            if user:
                # logged-in user → 300 token quota
                session = request.session
                used_tokens = session.get("user_tokens", 0)
                tokens_used = len(resume_text.split())
                if used_tokens + tokens_used > 300:
                    return Response({"error": "Token limit reached. Please upgrade."}, status=403)
                session["user_tokens"] = used_tokens + tokens_used
                session.save()
                remaining_tokens = 300 - session["user_tokens"]
            else:
                # guest user → 50 token quota
                session = request.session
                used_tokens = session.get("guest_tokens", 0)
                tokens_used = len(resume_text.split())
                if used_tokens + tokens_used > 50:
                    return Response({"error": "Free trial limit reached. Please login."}, status=403)
                session["guest_tokens"] = used_tokens + tokens_used
                session.save()
                remaining_tokens = 50 - session["guest_tokens"]

            # ✅ Flatten output
            result["remaining_tokens"] = remaining_tokens
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error during career analysis: {e}")
            return Response({"error": f"Failed to analyze resume: {e}"}, status=500)
