"""
Router for user-related operations.

This module defines the routes for user management,
including fetching user information, updating user details, and deleting users.

Routes:
    GET /users/me - Get information about the currently authenticated user.
    GET /users/{id} - Get user information by user ID (admin only).
    GET /users/ - Get a paginated list of users (admin only).
    PATCH /users/{id} - Update user information by user ID (admin only).
    DELETE /users/{id} - Delete user by user ID (admin only).

Classes:
    UserRouter: Class for handling user-related routes.
"""

from fastapi import Response, Depends
from core.di import DUoW, DUser, DUserAdmin
from routes.base import BaseRouter
from schemas import (
    CurrentUserSchema,
    UserSchema,
    PaginationRequestSchema,
    UserUpdateRequestSchema,
    BaseResponseSchema,
)
from schemas.v1.auth.exception import (
    TokenMissingResponseSchema,
    TokenExpiredResponseSchema,
    TokenInvalidResponseSchema,
)
from services.v1.user.service import UserService


class UserRouter(BaseRouter):
    """
    Router for user-related operations.

    Provides endpoints for:
    - Retrieving the current user's information.
    - Retrieving a user by ID (admin only).
    - Listing users with pagination (admin only).
    - Updating a user by ID (admin only).
    - Deleting a user by ID (admin only).
    """

    def __init__(self):
        super().__init__(prefix="users", tags=["Users"])

    def configure(self):

        @self.router.get(
            path="/me",
            response_model=CurrentUserSchema,
            summary="Get current user information",
            responses={
                200: {
                    "model": CurrentUserSchema,
                    "description": "Current user information retrieved successfully.",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Access token is missing.",
                },
                419: {
                    "model": TokenExpiredResponseSchema,
                    "description": "Access token has expired.",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Access token is invalid.",
                },
            },
        )
        async def get_me(
            user: DUser,
        ) -> CurrentUserSchema:
            """
            ## Get Current User Information

            Retrieves the information of the currently authenticated user.

            ### Returns:
            - **CurrentUserSchema**: The schema containing the current user's information.
            """
            return user

        @self.router.get(
            path="",
            response_model=list[UserSchema],
            summary="Get list of users (admin only)",
            responses={
                200: {
                    "model": list[UserSchema],
                    "description": "List of users retrieved successfully.",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Access token is missing.",
                },
                419: {
                    "model": TokenExpiredResponseSchema,
                    "description": "Access token has expired.",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Access token is invalid.",
                },
            },
        )
        async def get_users(
            uow: DUoW,
            user: DUserAdmin,
            pagination: PaginationRequestSchema = Depends(),
        ) -> list[UserSchema]:
            """
            ## Get List of Users (Admin Only)

            Retrieves a paginated list of users. This endpoint is accessible only to administrators.

            ### Parameters:
            - **pagination**: PaginationRequestSchema object for page and size.

            ### Returns:
            - **list[UserSchema]**: List of user objects.
            """
            return await UserService.get_users(
                uow=uow, pagination=pagination
            )

        @self.router.get(
            path="/{id}",
            response_model=UserSchema,
            summary="Get user information by ID",
            responses={
                200: {
                    "model": UserSchema,
                    "description": "Requested user's information retrieved successfully.",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Access token is missing.",
                },
                419: {
                    "model": TokenExpiredResponseSchema,
                    "description": "Access token has expired.",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Access token is invalid.",
                },
            },
        )
        async def get_user(
            uow: DUoW,
            user: DUser,
            user_id: int,
        ) -> UserSchema:
            """
            ## Get User Information by ID

            Retrieves information about a user by their ID

            ### Parameters:
            - **user_id** (int): The ID of the user to retrieve.

            ### Returns:
            - **UserSchema**: The schema containing the requested user's information.
            """
            return await UserService.get_user(uow=uow, user_id=user_id)

        @self.router.patch(
            path="/{id}",
            response_model=UserSchema,
            summary="Update user information by ID (admin only)",
            responses={
                200: {
                    "model": UserSchema,
                    "description": "User information updated successfully.",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Access token is missing.",
                },
                419: {
                    "model": TokenExpiredResponseSchema,
                    "description": "Access token has expired.",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Access token is invalid.",
                },
            },
        )
        async def update_user(
            uow: DUoW,
            user: DUserAdmin,
            user_id: int,
            form_data: UserUpdateRequestSchema,
        ) -> UserSchema:
            """
            ## Update User Information by ID (Admin Only)

            Updates the information of a user by their ID. Only accessible to administrators.

            ### Parameters:
            - **user_id** (int): The ID of the user to update.
            - **form_data** (UserUpdateRequestSchema): The data to update for the user.

            ### Returns:
            - **UserSchema**: The schema containing the updated user's information.
            """
            return await UserService.update_user(
                uow=uow, form_data=form_data, user_id=user_id
            )

        @self.router.delete(
            path="/{id}",
            response_model=BaseResponseSchema,
            summary="Delete user by ID (admin only)",
            responses={
                200: {
                    "model": BaseResponseSchema,
                    "description": "User deleted successfully.",
                },
                401: {
                    "model": TokenMissingResponseSchema,
                    "description": "Access token is missing.",
                },
                419: {
                    "model": TokenExpiredResponseSchema,
                    "description": "Access token has expired.",
                },
                422: {
                    "model": TokenInvalidResponseSchema,
                    "description": "Access token is invalid.",
                },
            },
        )
        async def delete_user(
            response: Response,
            uow: DUoW,
            user: DUserAdmin,
            user_id: int,
        ) -> BaseResponseSchema:
            """
            ## Delete User by ID (Admin Only)

            Deletes a user by their ID. Only accessible to administrators.

            ### Parameters:
            - **user_id** (int): The ID of the user to delete.

            ### Returns:
            - **BaseResponseSchema**: Response indicating success or failure of the deletion.
            """
            return await UserService.delete_user(
                uow=uow, user_id=user_id, response=response
            )
