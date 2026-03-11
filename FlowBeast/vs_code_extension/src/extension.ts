import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('datacody.compile', async () => {
        const token = vscode.workspace.getConfiguration('datacody').get<string>('token');
        if (!token) {
            const email = await vscode.window.showInputBox({ prompt: "输入邮箱登录 DataCody" });
            const res = await axios.post('http://localhost:8000/v1/auth/login', { email, password: 'dummy' });
            vscode.workspace.getConfiguration('datacody').update('token', res.data.access_token, true);
            vscode.window.showInformationMessage('登录成功！');
            return;
        }

        const task = await vscode.window.showInputBox({ prompt: "输入数据任务" });
        if (!task) return;

        try {
            const res = await axios.post('http://localhost:8000/v1/compile', { task }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            const doc = await vscode.workspace.openTextDocument({ content: res.data.code, language: 'python' });
            vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage(`编译成功，消耗 ${res.data.cost_units} 单位`);
        } catch (e) {
            if (e.response.status === 429) {
                vscode.window.showErrorMessage('配额不足，点击升级');
                vscode.env.openExternal(vscode.Uri.parse('http://localhost:8000/v1/billing/checkout'));
            }
        }
    });
    context.subscriptions.push(disposable);
}
