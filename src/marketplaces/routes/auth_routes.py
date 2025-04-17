# src/routes/auth_routes.py

@router.post("/register-vendor")
async def register_vendor(form_data: Request, db: Session = Depends(get_db)):
    form = await form_data.form()
        vendor_id = str(uuid.uuid4())
            db.add(Vendor(id=vendor_id, name=form['name'], description=form['description']))
                
                    user = User(
                            id=str(uuid.uuid4()),
                                    email=form['email'],
                                            hashed_password=hash_password(form['password']),
                                                    role="admin",
                                                            vendor_id=vendor_id
                                                                )
                                                                    db.add(user)
                                                                        db.commit()
                                                                            return RedirectResponse("/login", status_code=303)
