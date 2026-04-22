from aiogram import Bot, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import router
from database import SessionLocal, Transaction, FinancialGoal, User
from sqlalchemy import desc
from keyboardsHelper import secretary_kb, main_kb

class FinanceStates(StatesGroup):
    Main_menu = State()
    Adding_expense = State()
    Adding_expense_desc = State()
    Adding_income = State()
    Adding_income_desc = State()
    Setting_goal = State()
    Setting_goal_desc = State()


@router.message(F.text.in_(["/Secretary", "секретарь"]))
async def cmd_secretary(message: Message, state: FSMContext):
    await message.answer("Финансовый помощник", reply_markup=secretary_kb)
    await state.set_state(FinanceStates.Main_menu)


@router.message(FinanceStates.Main_menu, F.text == "Потратить")
async def add_expense(message: Message, state: FSMContext):
    await message.answer("Введите сумму траты (число):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FinanceStates.Adding_expense)


@router.message(FinanceStates.Adding_expense)
async def process_expense(message: Message, state: FSMContext):
    try:
        amount = float(message.text or 0)
        if amount <= 0:
            await message.answer("Сумма должна быть больше нуля!")
            return

        await state.update_data(amount=amount)
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустить")]], resize_keyboard=True)
        await message.answer("Введите описание или 'Пропустить':", reply_markup=kb)
        await state.set_state(FinanceStates.Adding_expense_desc)
    except ValueError:
        await message.answer("Неверный формат. Введите число:")


@router.message(FinanceStates.Adding_expense_desc)
async def process_expense_description(message: Message, state: FSMContext):
    description = None if message.text == "Пропустить" else message.text
    data = await state.get_data()
    amount = data.get('amount')
    if amount is None:
        await message.answer("Не найдена сумма. Повторите ввод траты.")
        await state.set_state(FinanceStates.Main_menu)
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == message.from_user.id).first()
        if not user:
            user = User(user_id=message.from_user.id, first_name=message.from_user.first_name or '')
            db.add(user)
            db.commit()

        transaction = Transaction(
            user_id=message.from_user.id,
            amount=-abs(amount),  # отрицательная сумма для траты
            description=description,
            transaction_type="expense"
        )
        db.add(transaction)
        db.commit()

        await message.answer(f"Трата добавлена: -{amount}", reply_markup=secretary_kb)
        await state.set_state(FinanceStates.Main_menu)
    except Exception as e:
        db.rollback()
        await message.answer(f"Ошибка: {e}")
    finally:
        db.close()


@router.message(FinanceStates.Main_menu, F.text == "Добавить доход")
async def add_income(message: Message, state: FSMContext):
    await message.answer("Введите сумму дохода (число):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FinanceStates.Adding_income)


@router.message(FinanceStates.Adding_income)
async def process_income(message: Message, state: FSMContext):
    try:
        amount = float(message.text or 0)
        if amount <= 0:
            await message.answer("Сумма должна быть больше нуля!")
            return

        await state.update_data(amount=amount)
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустить")]], resize_keyboard=True)
        await message.answer("Введите описание или 'Пропустить':", reply_markup=kb)
        await state.set_state(FinanceStates.Adding_income_desc)
    except ValueError:
        await message.answer("Неверный формат. Введите число:")


@router.message(FinanceStates.Adding_income_desc)
async def process_income_description(message: Message, state: FSMContext):
    description = None if message.text == "Пропустить" else message.text
    data = await state.get_data()
    amount = data.get('amount')
    if amount is None:
        await message.answer("Не найдена сумма. Повторите ввод дохода.")
        await state.set_state(FinanceStates.Main_menu)
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == message.from_user.id).first()
        if not user:
            user = User(user_id=message.from_user.id, first_name=message.from_user.first_name or '')
            db.add(user)
            db.commit()

        transaction = Transaction(
            user_id=message.from_user.id,
            amount=abs(amount),
            description=description,
            transaction_type="income"
        )
        db.add(transaction)
        db.commit()
        goal = db.query(FinancialGoal).filter(FinancialGoal.user_id == message.from_user.id).first()
        if goal is not None:
         goal.current_amount = (goal.current_amount or 0) + abs(amount)
         db.commit()

        await message.answer(f"Доход добавлен: +{amount}", reply_markup=secretary_kb)
        await state.set_state(FinanceStates.Main_menu)
    except Exception as e:
        db.rollback()
        await message.answer(f"Ошибка: {e}")
    finally:
        db.close()


@router.message(FinanceStates.Main_menu, F.text == "Установить цель")
async def set_goal(message: Message, state: FSMContext):
    await message.answer("Введите сумму цели (число):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FinanceStates.Setting_goal)


@router.message(FinanceStates.Setting_goal)
async def process_goal_amount(message: Message, state: FSMContext):
    try:
        goal_amount = float(message.text or 0)
        if goal_amount <= 0:
            await message.answer("Сумма должна быть больше нуля!")
            return

        await state.update_data(goal_amount=goal_amount)
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустить")]], resize_keyboard=True)
        await message.answer("Введите описание цели или 'Пропустить':", reply_markup=kb)
        await state.set_state(FinanceStates.Setting_goal_desc)
    except ValueError:
        await message.answer("Неверный формат. Введите число:")


@router.message(FinanceStates.Setting_goal_desc)
async def process_goal_description(message: Message, state: FSMContext):
    description = None if message.text == "Пропустить" else message.text
    data = await state.get_data()
    goal_amount = data.get('goal_amount')
    if goal_amount is None:
        await message.answer("Не найдена сумма цели. Повторите установку цели.")
        await state.set_state(FinanceStates.Main_menu)
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == message.from_user.id).first()
        if not user:
            user = User(user_id=message.from_user.id, first_name=message.from_user.first_name or '')
            db.add(user)
            db.commit()

        existing_goal = db.query(FinancialGoal).filter(FinancialGoal.user_id == message.from_user.id).first()
        if existing_goal:
            existing_goal.goal_amount = goal_amount
            existing_goal.description = description
        else:
            new_goal = FinancialGoal(user_id=message.from_user.id, goal_amount=goal_amount, description=description)
            db.add(new_goal)
        db.commit()

        await message.answer(f"Цель обновлена/установлена: {goal_amount}", reply_markup=secretary_kb)
        await state.set_state(FinanceStates.Main_menu)
    except Exception as e:
        db.rollback()
        await message.answer(f"Ошибка: {e}")
    finally:
        db.close()


@router.message(FinanceStates.Main_menu, F.text == "Мой баланс")
async def show_balance(message: Message, state: FSMContext):
    db = SessionLocal()
    try:
        transactions = db.query(Transaction).filter(Transaction.user_id == message.from_user.id).all()
        total_balance = sum(t.amount for t in transactions) if transactions else 0

        goal = db.query(FinancialGoal).filter(FinancialGoal.user_id == message.from_user.id).first()

        response = f"**Твой баланс:**\n"
        response += f"Общая сумма: `{total_balance:.2f}`\n"

        if goal:
            response += f"\n**Цель:**\n"
            response += f"Нужно собрать: `{goal.goal_amount:.2f}`\n"
            response += f"Прогресс: `{goal.current_amount:.2f}` / `{goal.goal_amount:.2f}`\n"
            if goal.description:
                response += f"Описание: `{goal.description}`"
        else:
            response += f"\n(Цель не установлена)"

        await message.answer(response)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        db.close()


@router.message(FinanceStates.Main_menu, F.text == "История")
async def show_history(message: Message, state: FSMContext):
    db = SessionLocal()
    try:
        transactions = db.query(Transaction).filter(
            Transaction.user_id == message.from_user.id
        ).order_by(desc(Transaction.created_at)).limit(20).all()

        if not transactions:
            await message.answer("История пуста")
            return

        response = "**История последних 20 транзакций:**\n\n"
        for t in transactions:
            sign = "+" if t.amount > 0 else "-"
            response += f"{sign} {abs(t.amount):.2f}"
            if t.description:
                response += f" - {t.description}"
            response += f" ({t.created_at.strftime('%d.%m %H:%M')})\n"

        await message.answer(response)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        db.close()


@router.message(FinanceStates.Main_menu, F.text == "Назад")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "КОМАНДЫ:\n/remind - взаимодействие с напоминаниями \n/secretchat - отправить секретное сообщение\n/Secretary - финансовый помощник\n/timer - установить таймер",
        reply_markup=main_kb
    )
